import asyncio
import json
import os
import hashlib
import secrets
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path
import socket
import subprocess
import signal
import sys

from fastapi import FastAPI, Request, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

# ─── تنظیمات لاگ ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("Eagle-Gateway")

IRAN_TZ = ZoneInfo("Asia/Tehran")

# ─── کانفیگ ──────────────────────────────────────────────────────────────────
CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": os.environ.get("SECRET_KEY", secrets.token_urlsafe(32)),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
    "admin_password": os.environ.get("ADMIN_PASSWORD", "123456"),
}

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="🦅 Eagle Gateway v10 Pro", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── State ────────────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "eagle_state.json"
SAVE_LOCK = asyncio.Lock()

# ─── In-Memory State ─────────────────────────────────────────────────────────
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()
connections: dict = {}
stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
device_connections: dict = {}
DEVICE_CONNECTIONS_LOCK = asyncio.Lock()
http_client: httpx.AsyncClient | None = None

# ─── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "eagle_session"
SESSION_TTL = 60 * 60 * 24 * 7
AUTH = {"password_hash": hashlib.sha256(f"{CONFIG['admin_password']}{CONFIG['secret']}".encode()).hexdigest()}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

# ─── Settings ──────────────────────────────────────────────────────────────────
SETTINGS: dict = {
    "rgb_mode": False,
    "telegram_token": None,
    "telegram_chat_id": None,
    "telegram_enabled": False,
    "telegram_bot_running": False,
    "telegram_bot_pid": None,
    "telegram_allowed_users": [],
    "default_protocol": "vless-ws",
    "default_port": 443,
}

PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one")
DEFAULT_PROTOCOL = "vless-ws"

# ─── Functions ─────────────────────────────────────────────────────────────────

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def fmt_bytes(b: int) -> str:
    if not b or b == 0:
        return "0 B"
    if b < 1024:
        return f"{b} B"
    if b < 1024**2:
        return f"{b/1024:.1f} KB"
    if b < 1024**3:
        return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB":
        return int(value * 1024 ** 3)
    if unit == "MB":
        return int(value * 1024 ** 2)
    if unit == "KB":
        return int(value * 1024)
    return int(value)

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True

def generate_vless_link(uuid: str, host: str, remark: str = "", protocol: str = DEFAULT_PROTOCOL, 
                        fingerprint: str = "chrome", port: int = 443) -> str:
    if not remark:
        remark = "عقاب"
    
    if protocol == "vless-ws":
        path = f"/ws/{uuid}"
        params = {
            "encryption": "none",
            "security": "tls",
            "type": "ws",
            "host": host,
            "path": path,
            "sni": host,
            "fp": fingerprint,
            "alpn": "http/1.1",
        }
    else:
        mode = protocol.replace("xhttp-", "")
        path = f"/xhttp-siz10/{mode}/{uuid}"
        params = {
            "encryption": "none",
            "security": "tls",
            "type": "xhttp",
            "mode": mode,
            "host": host,
            "path": path,
            "sni": host,
            "fp": fingerprint,
            "alpn": "h2,http/1.1",
        }
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{host}:{port}?{query}#{quote(remark)}"

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

async def remove_device_connection(uuid: str, client_ip: str):
    async with DEVICE_CONNECTIONS_LOCK:
        if uuid in device_connections:
            if client_ip in device_connections[uuid]:
                device_connections[uuid].remove(client_ip)
                if not device_connections[uuid]:
                    del device_connections[uuid]

# ─── Telegram Bot Integration ─────────────────────────────────────────────────

async def send_telegram_message(message: str) -> bool:
    if not SETTINGS.get("telegram_enabled"):
        return False
    
    token = SETTINGS.get("telegram_token")
    chat_id = SETTINGS.get("telegram_chat_id")
    
    if not token or not chat_id:
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            resp = await client.post(url, json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            })
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False

async def start_bot_process():
    try:
        if SETTINGS.get("telegram_bot_running", False):
            return True
        
        env = os.environ.copy()
        env["PANEL_URL"] = f"http://localhost:{CONFIG['port']}"
        env["ADMIN_PASSWORD"] = CONFIG["admin_password"]
        env["TELEGRAM_BOT_TOKEN"] = SETTINGS.get("telegram_token", "")
        
        allowed_users = SETTINGS.get("telegram_allowed_users", [])
        if allowed_users:
            env["ALLOWED_USERS"] = ",".join(str(u) for u in allowed_users)
        
        proc = subprocess.Popen(
            [sys.executable, "telegram_bot.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            env=env
        )
        
        SETTINGS["telegram_bot_pid"] = proc.pid
        SETTINGS["telegram_bot_running"] = True
        await save_state()
        
        logger.info(f"✅ ربات تلگرام با PID {proc.pid} استارت خورد")
        return True
    except Exception as e:
        logger.error(f"❌ خطا در استارت ربات: {e}")
        SETTINGS["telegram_bot_running"] = False
        return False

async def stop_bot_process():
    try:
        pid = SETTINGS.get("telegram_bot_pid")
        if pid:
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
            SETTINGS["telegram_bot_pid"] = None
        
        SETTINGS["telegram_bot_running"] = False
        await save_state()
        logger.info("✅ ربات تلگرام متوقف شد")
        return True
    except Exception as e:
        logger.error(f"❌ خطا در توقف ربات: {e}")
        return False

async def send_telegram_link_created(link_data: dict):
    if not SETTINGS.get("telegram_enabled"):
        return
    
    host = get_host()
    msg = f"""🦅 <b>کانفیگ جدید ساخته شد!</b>

📌 <b>نام:</b> {link_data.get('label', 'نامشخص')}
🔑 <b>UUID:</b> <code>{link_data.get('uuid', '')}</code>
📊 <b>حجم:</b> {fmt_bytes(link_data.get('limit_bytes', 0))}
📱 <b>دستگاه‌ها:</b> {link_data.get('max_devices', 0)}
📅 <b>انقضا:</b> {link_data.get('expires_at', 'نامحدود')}

🔗 <b>لینک اشتراک:</b>
<code>https://{host}/sub/{link_data.get('uuid', '')}</code>
"""
    await send_telegram_message(msg)

# ─── Session Functions ──────────────────────────────────────────────────────

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

# ─── State Persistence ──────────────────────────────────────────────────────

async def load_state():
    global LINKS, SUBS, AUTH, SETTINGS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            if "settings" in data:
                SETTINGS.update(data["settings"])
            logger.info(f"📂 State loaded: {len(LINKS)} links, {len(SUBS)} subs")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "password_hash": AUTH["password_hash"],
                "settings": SETTINGS,
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ─── Startup / Shutdown ─────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True)
    await load_state()
    
    if SETTINGS.get("telegram_enabled") and SETTINGS.get("telegram_token"):
        await start_bot_process()
        await send_telegram_message("🦅 <b>پنل عقاب راه‌اندازی شد!</b>\n\n✅ سرور با موفقیت استارت خورد.")
    
    log_activity("system", "🦅 پنل عقاب v10 Pro راه‌اندازی شد", "ok")
    logger.info(f"🦅 Eagle Gateway v10 Pro started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client:
        await http_client.aclose()
    
    if SETTINGS.get("telegram_bot_running"):
        await stop_bot_process()

# ─── API: Telegram Bot Management ────────────────────────────────────────────

@app.get("/api/telegram/status")
async def get_telegram_status(_=Depends(require_auth)):
    return {
        "enabled": SETTINGS.get("telegram_enabled", False),
        "running": SETTINGS.get("telegram_bot_running", False),
        "token_set": bool(SETTINGS.get("telegram_token")),
        "chat_id_set": bool(SETTINGS.get("telegram_chat_id")),
        "allowed_users": SETTINGS.get("telegram_allowed_users", []),
    }

@app.post("/api/telegram/toggle")
async def toggle_telegram_bot(request: Request, _=Depends(require_auth)):
    body = await request.json()
    enabled = bool(body.get("enabled", False))
    token = body.get("token", "").strip()
    chat_id = body.get("chat_id", "").strip()
    allowed_users = body.get("allowed_users", [])
    
    if enabled and (not token or not chat_id):
        raise HTTPException(status_code=400, detail="برای فعال‌سازی، توکن و چت‌آیدی الزامی است")
    
    SETTINGS["telegram_token"] = token if token else None
    SETTINGS["telegram_chat_id"] = chat_id if chat_id else None
    SETTINGS["telegram_enabled"] = enabled
    SETTINGS["telegram_allowed_users"] = allowed_users if isinstance(allowed_users, list) else []
    
    if enabled:
        test_msg = await send_telegram_message("🦅 <b>ربات پنل عقاب در حال راه‌اندازی...</b>")
        if not test_msg:
            SETTINGS["telegram_enabled"] = False
            await save_state()
            raise HTTPException(status_code=400, detail="ارسال پیام تست ناموفق! توکن یا چت‌آیدی اشتباه است.")
        
        if not SETTINGS.get("telegram_bot_running"):
            await start_bot_process()
        
        await send_telegram_message("✅ <b>ربات پنل عقاب با موفقیت فعال شد!</b>")
        
    else:
        await stop_bot_process()
        SETTINGS["telegram_enabled"] = False
    
    await save_state()
    log_activity("telegram", f"ربات تلگرام {'فعال' if enabled else 'غیرفعال'} شد", "info")
    
    return {
        "ok": True,
        "settings": {
            "telegram_enabled": SETTINGS["telegram_enabled"],
            "telegram_bot_running": SETTINGS.get("telegram_bot_running", False),
            "telegram_token_set": bool(SETTINGS.get("telegram_token")),
            "telegram_chat_id_set": bool(SETTINGS.get("telegram_chat_id")),
            "allowed_users": SETTINGS.get("telegram_allowed_users", []),
        }
    }

@app.post("/api/telegram/send_test")
async def send_test_message(request: Request, _=Depends(require_auth)):
    msg = "🦅 <b>پیام تست از پنل عقاب</b>\n\n✅ اتصال برقرار است."
    result = await send_telegram_message(msg)
    if result:
        return {"ok": True, "message": "پیام تست ارسال شد"}
    else:
        raise HTTPException(status_code=400, detail="ارسال پیام تست ناموفق!")

# ─── API: Settings ─────────────────────────────────────────────────────────

@app.get("/api/settings")
async def get_settings(_=Depends(require_auth)):
    return {
        **SETTINGS,
        "telegram_token_set": bool(SETTINGS.get("telegram_token")),
        "telegram_chat_id_set": bool(SETTINGS.get("telegram_chat_id")),
    }

@app.post("/api/settings/rgb")
async def toggle_rgb(request: Request, _=Depends(require_auth)):
    body = await request.json()
    SETTINGS["rgb_mode"] = bool(body.get("enabled", False))
    await save_state()
    return {"rgb_mode": SETTINGS["rgb_mode"]}

@app.post("/api/settings/password")
async def change_password(request: Request, _=Depends(require_auth)):
    body = await request.json()
    old_password = body.get("old_password", "").strip()
    new_password = body.get("new_password", "").strip()
    
    if not old_password or not new_password:
        raise HTTPException(status_code=400, detail="رمز فعلی و جدید الزامی است")
    
    if len(new_password) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل 4 کاراکتر باشد")
    
    if hash_password(old_password) != AUTH["password_hash"]:
        raise HTTPException(status_code=403, detail="رمز فعلی اشتباه است")
    
    AUTH["password_hash"] = hash_password(new_password)
    CONFIG["admin_password"] = new_password
    os.environ["ADMIN_PASSWORD"] = new_password
    
    await save_state()
    log_activity("settings", "رمز پنل تغییر کرد", "ok")
    
    await send_telegram_message(f"🔑 <b>رمز پنل تغییر کرد!</b>\n\n🔐 رمز جدید: <code>{new_password}</code>")
    
    return {"ok": True, "message": "رمز با موفقیت تغییر کرد"}

# ─── API: Links ─────────────────────────────────────────────────────────────

@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    label = (body.get("label") or "لینک جدید").strip()[:60]
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    note = (body.get("note") or "").strip()[:200]
    sub_id = body.get("sub_id") or None
    protocol = body.get("protocol") or DEFAULT_PROTOCOL
    if protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL
    max_devices = int(body.get("max_devices", 0))
    fingerprint = body.get("fingerprint", "chrome")
    config_password = body.get("password", "").strip()
    password_hash = hash_password(config_password) if config_password else None
    port = int(body.get("port", 443))
    if port < 1 or port > 65535:
        port = 443

    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": label,
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": note,
            "is_default": False,
            "sub_id": sub_id,
            "protocol": protocol,
            "max_devices": max_devices,
            "fingerprint": fingerprint,
            "password_hash": password_hash,
            "port": port,
        }

    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{label}» ساخته شد", "ok")
    host = get_host()
    
    remark = f"عقاب-{label}"
    main_link = generate_vless_link(uid, host, remark=remark, protocol=protocol, fingerprint=fingerprint, port=port)
    
    link_data = {
        "uuid": uid,
        **LINKS[uid],
        "has_password": password_hash is not None,
        "vless_link": main_link,
        "sub_url": f"https://{host}/sub/{uid}",
        "warning_config": "",
    }
    
    asyncio.create_task(send_telegram_link_created(link_data))
    
    return link_data

@app.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = get_host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    
    result = []
    for uid, d in snap.items():
        proto = d.get("protocol", DEFAULT_PROTOCOL)
        fp = d.get("fingerprint", "chrome")
        port = d.get("port", 443)
        label = d.get("label", "کاربر")
        remark = f"عقاب-{label}"
        
        last_connected = None
        for c in connections.values():
            if c.get("uuid") == uid:
                if not last_connected or c.get("connected_at") > last_connected:
                    last_connected = c.get("connected_at")
        
        result.append({
            "uuid": uid,
            **d,
            "protocol": proto,
            "fingerprint": fp,
            "max_devices": d.get("max_devices", 0),
            "expired": is_link_expired(d),
            "has_password": d.get("password_hash") is not None,
            "port": port,
            "last_connected_at": last_connected,
            "vless_link": generate_vless_link(uid, host, remark=remark, protocol=proto, fingerprint=fp, port=port),
            "sub_url": f"https://{host}/sub/{uid}",
            "warning_config": "",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        
        if link.get("password_hash"):
            password = body.get("password", "").strip()
            if not password:
                raise HTTPException(status_code=403, detail="برای ویرایش این کانفیگ رمز آن را وارد کنید")
            if hash_password(password) != link["password_hash"]:
                raise HTTPException(status_code=403, detail="رمز کانفیگ اشتباه است")
        
        old_sub = link.get("sub_id")
        
        if "active" in body:
            link["active"] = bool(body["active"])
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "max_devices" in body:
            link["max_devices"] = int(body["max_devices"])
        if "fingerprint" in body:
            link["fingerprint"] = str(body["fingerprint"])
        if "protocol" in body and body["protocol"] in PROTOCOLS:
            link["protocol"] = body["protocol"]
        if "port" in body:
            port = int(body["port"])
            if 1 <= port <= 65535:
                link["port"] = port
        new_sub = body.get("sub_id", "UNCHANGED")
        if new_sub != "UNCHANGED":
            link["sub_id"] = new_sub or None

    if new_sub != "UNCHANGED":
        async with SUBS_LOCK:
            if old_sub and old_sub in SUBS:
                ids = SUBS[old_sub].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
            if new_sub and new_sub in SUBS:
                ids = SUBS[new_sub].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)

    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{link['label']}» ویرایش شد", "info")
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    password = body.get("password", "").strip()
    
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        
        if link.get("password_hash"):
            if not password:
                raise HTTPException(status_code=403, detail="برای حذف این کانفیگ رمز آن را وارد کنید")
            if hash_password(password) != link["password_hash"]:
                raise HTTPException(status_code=403, detail="رمز کانفیگ اشتباه است")
        
        label = link.get("label", uid)
        sub_id = link.get("sub_id")
        del LINKS[uid]
    
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{label}» حذف شد", "err")
    
    await send_telegram_message(f"🗑️ <b>کانفیگ حذف شد</b>\n\n📌 نام: {label}\n🔑 UUID: <code>{uid}</code>")
    
    return {"ok": True, "deleted": uid}

# ─── API: Subs ─────────────────────────────────────────────────────────────

@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name": name,
            "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
        }
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» ساخته شد", "ok")
    host = get_host()
    
    await send_telegram_message(f"📁 <b>گروه اشتراک جدید</b>\n\n📌 نام: {name}\n🔗 لینک: https://{host}/sub-group/{uuid_key}")
    
    return {
        "sub_id": sub_id,
        **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}",
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
    }

@app.get("/api/subs")
async def list_subs(_=Depends(require_auth)):
    host = get_host()
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = sum(1 for lid in link_ids if is_link_allowed(snap_links.get(lid)))
        total_used = sum(snap_links[lid].get("used_bytes", 0) for lid in link_ids if lid in snap_links)
        result.append({
            "sub_id": sid,
            **s,
            "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "links_count": len(link_ids),
            "active_count": active_count,
            "total_used_bytes": total_used,
            "total_used_fmt": fmt_bytes(total_used),
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body:
            s["link_ids"] = list(body["link_ids"])
    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id:
                link["sub_id"] = None
    asyncio.create_task(save_state())
    log_activity("sub", f"گروه «{name}» حذف شد", "warn")
    
    await send_telegram_message(f"🗑️ <b>گروه اشتراک حذف شد</b>\n\n📌 نام: {name}")
    
    return {"ok": True, "deleted": sub_id}

# ─── API: Stats & Connections ──────────────────────────────────────────────

@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    
    top_user = None
    top_usage = 0
    for uid, link in snap.items():
        used = link.get("used_bytes", 0)
        if used > top_usage:
            top_usage = used
            top_user = {
                "uuid": uid,
                "label": link.get("label", "نامشخص"),
                "used_bytes": used,
                "used_fmt": fmt_bytes(used)
            }
    
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS),
        "top_user": top_user,
    }

@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)

    grouped: dict[str, dict] = {}
    for conn_id, c in connections.items():
        ip = c.get("ip", "نامشخص")
        link = snap.get(c.get("uuid"))
        label = link.get("label") if link else "نامشخص"
        g = grouped.get(ip)
        if g is None:
            g = {
                "ip": ip,
                "sessions": 0,
                "bytes": 0,
                "labels": set(),
                "transports": set(),
                "first_connected_at": c.get("connected_at"),
                "last_connected_at": c.get("connected_at"),
            }
            grouped[ip] = g
        g["sessions"] += 1
        g["bytes"] += c.get("bytes", 0)
        g["labels"].add(label)
        g["transports"].add(c.get("transport", "vless-ws"))
        ca = c.get("connected_at")
        if ca:
            if not g["first_connected_at"] or ca < g["first_connected_at"]:
                g["first_connected_at"] = ca
            if not g["last_connected_at"] or ca > g["last_connected_at"]:
                g["last_connected_at"] = ca

    result = []
    for ip, g in grouped.items():
        result.append({
            "ip": ip,
            "sessions": g["sessions"],
            "labels": sorted(g["labels"]),
            "label": " · ".join(sorted(g["labels"])) if g["labels"] else "نامشخص",
            "transports": sorted(g["transports"]),
            "bytes": g["bytes"],
            "bytes_fmt": fmt_bytes(g["bytes"]),
            "connected_at": g["first_connected_at"],
            "last_connected_at": g["last_connected_at"],
        })
    result.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)

    return {
        "connections": result,
        "count": len(result),
        "raw_count": len(connections),
    }

# ─── Auth Endpoints ────────────────────────────────────────────────────────

@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

# ─── Backup ────────────────────────────────────────────────────────────────────

@app.get("/api/backup")
async def get_backup(_=Depends(require_auth)):
    async with LINKS_LOCK:
        links = dict(LINKS)
    async with SUBS_LOCK:
        subs = dict(SUBS)
    return {
        "links": links,
        "subs": subs,
        "password_hash": AUTH["password_hash"],
        "settings": SETTINGS,
        "exported_at": datetime.now().isoformat(),
        "version": "10.0"
    }

@app.post("/api/backup/restore")
async def restore_backup(request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
        
        if "links" in body and isinstance(body["links"], dict):
            async with LINKS_LOCK:
                LINKS.clear()
                for uid, link_data in body["links"].items():
                    if not isinstance(link_data, dict):
                        continue
                    LINKS[uid] = link_data
        
        if "subs" in body and isinstance(body["subs"], dict):
            async with SUBS_LOCK:
                SUBS.clear()
                for sid, sub_data in body["subs"].items():
                    if not isinstance(sub_data, dict):
                        continue
                    SUBS[sid] = sub_data
        
        if "password_hash" in body:
            AUTH["password_hash"] = body["password_hash"]
        
        if "settings" in body and isinstance(body["settings"], dict):
            SETTINGS.update(body["settings"])
        
        await save_state()
        log_activity("backup", "بکاپ بازیابی شد", "ok")
        await send_telegram_message("🔄 <b>بکاپ با موفقیت بازیابی شد</b>")
        return {"ok": True, "message": "بکاپ با موفقیت بازیابی شد"}
    except Exception as e:
        logger.error(f"Backup restore error: {e}")
        raise HTTPException(status_code=400, detail=f"خطا در بازیابی بکاپ: {str(e)}")

# ─── VLESS WebSocket Tunnel ────────────────────────────────────────────────

RELAY_BUF = 256 * 1024

def _ws_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = ws.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return ws.client.host if ws.client else "نامشخص"

async def check_device_limit(uuid: str, client_ip: str) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link:
            return False
        max_devices = link.get("max_devices", 0)
        if max_devices == 0:
            return True
    
    async with DEVICE_CONNECTIONS_LOCK:
        current_ips = device_connections.get(uuid, [])
        if client_ip in current_ips:
            return True
        if len(current_ips) >= max_devices:
            return False
        if uuid not in device_connections:
            device_connections[uuid] = []
        device_connections[uuid].append(client_ip)
        return True

async def parse_vless_header(chunk: bytes):
    if len(chunk) < 24:
        raise ValueError("chunk too small")
    pos = 1
    pos += 16
    addon_len = chunk[pos]
    pos += 1 + addon_len
    command = chunk[pos]
    pos += 1
    port = int.from_bytes(chunk[pos:pos+2], "big")
    pos += 2
    addr_type = chunk[pos]
    pos += 1
    if addr_type == 1:
        address = ".".join(str(b) for b in chunk[pos:pos+4])
        pos += 4
    elif addr_type == 2:
        dlen = chunk[pos]
        pos += 1
        address = chunk[pos:pos+dlen].decode("utf-8", errors="ignore")
        pos += dlen
    elif addr_type == 3:
        ab = chunk[pos:pos+16]
        pos += 16
        address = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown addr type: {addr_type}")
    return command, address, port, chunk[pos:]

async def check_and_use(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] = link.get("used_bytes", 0) + n
        stats["total_bytes"] = stats.get("total_bytes", 0) + n
        hourly_traffic[now_ir().strftime("%H:00")] = hourly_traffic.get(now_ir().strftime("%H:00"), 0) + n
        
        limit = link.get("limit_bytes", 0)
        used = link.get("used_bytes", 0)
        if limit > 0 and used >= limit * 0.9 and used < limit:
            asyncio.create_task(send_telegram_message(
                f"⚠️ <b>هشدار مصرف</b>\n\n"
                f"📌 کاربر: {link.get('label', 'نامشخص')}\n"
                f"📊 مصرف: {used / (1024**3):.2f} GB از {limit / (1024**3):.2f} GB\n"
                f"🔴 <b>{((used / limit) * 100):.1f}%</b>"
            ))
    return True

async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str):
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            stats["total_requests"] = stats.get("total_requests", 0) + 1
            if conn_id in connections:
                connections[conn_id]["bytes"] = connections[conn_id].get("bytes", 0) + len(data)
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
    except (WebSocketDisconnect, Exception):
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass

async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            if conn_id in connections:
                connections[conn_id]["bytes"] = connections[conn_id].get("bytes", 0) + len(data)
            payload = (b"\x00\x00" + data) if first else data
            first = False
            await ws.send_bytes(payload)
    except Exception:
        pass

@app.websocket("/ws/{uuid}")
async def websocket_tunnel(ws: WebSocket, uuid: str):
    await ws.accept()

    client_ip = _ws_client_ip(ws)
    
    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not link:
        logger.warning(f"🚫 WS rejected uuid={uuid[:8]}… (user not found)")
        await ws.close(code=1008, reason="user not found")
        return

    if not is_link_allowed(link):
        logger.warning(f"🚫 WS rejected uuid={uuid[:8]}… (not allowed)")
        await ws.close(code=1008, reason="not authorized")
        return

    max_devices = link.get("max_devices", 0)
    if max_devices > 0:
        if not await check_device_limit(uuid, client_ip):
            logger.warning(f"🚫 Device limit exceeded for {uuid[:8]}… (max: {max_devices})")
            await ws.close(code=1008, reason="device limit exceeded")
            return

    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uuid,
        "ip": client_ip,
        "transport": "vless-ws",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    
    logger.info(f"✅ WS [{conn_id}] uuid={uuid[:8]}… ip={client_ip} total={len(connections)}")
    log_activity("connection", f"اتصال جدید از {client_ip} (کانفیگ {link.get('label','?')})", "info")
    
    asyncio.create_task(send_telegram_message(
        f"🔌 <b>اتصال جدید</b>\n\n"
        f"📌 کاربر: {link.get('label', 'نامشخص')}\n"
        f"🌐 IP: {client_ip}\n"
        f"⏱️ زمان: {datetime.now().strftime('%H:%M:%S')}"
    ))
    
    writer = None

    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            return

        command, address, port, payload = await parse_vless_header(first_chunk)

        if not await check_and_use(uuid, len(first_chunk)):
            await ws.close(code=1008, reason="quota/disabled")
            return

        stats["total_requests"] = stats.get("total_requests", 0) + 1
        if conn_id in connections:
            connections[conn_id]["bytes"] = connections[conn_id].get("bytes", 0) + len(first_chunk)
        logger.info(f"➡️  [{conn_id}] → {address}:{port}")

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=10.0
        )
        sock = writer.transport.get_extra_info('socket')
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        if payload:
            writer.write(payload)
            await writer.drain()

        done, pending = await asyncio.wait(
            {
                asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uuid)),
                asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uuid)),
            },
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except asyncio.CancelledError:
                pass

        asyncio.create_task(save_state())

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] = stats.get("total_errors", 0) + 1
        error_logs.append({"error": "connection timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] = stats.get("total_errors", 0) + 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"WS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        connections.pop(conn_id, None)
        await remove_device_connection(uuid, client_ip)
        logger.info(f"🔌 WS closed [{conn_id}] total={len(connections)}")

# ─── Subscriptions ─────────────────────────────────────────────────────────

@app.get("/sub/{uuid}")
async def subscription_single(uuid: str):
    from pages import get_sub_page_html
    
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    
    if not link:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🦅 کاربر یافت نشد</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;800&display=swap" rel="stylesheet">
        <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Vazirmatn',sans-serif;background:#0a0a0f;min-height:100vh;display:flex;align-items:center;justify-content:center;color:#F0F0FF}
        .card{background:rgba(15,15,30,0.85);backdrop-filter:blur(30px);border:1px solid rgba(59,130,246,0.12);border-radius:28px;padding:40px;max-width:420px;text-align:center}
        .icon{font-size:64px;margin-bottom:16px}
        h2{font-size:22px;font-weight:800;margin-bottom:8px}
        p{color:#6A6A8A;font-size:13px;line-height:1.8}
        </style>
        </head>
        <body>
        <div class="card">
            <div class="icon">🦅</div>
            <h2>کاربر یافت نشد</h2>
            <p>لینک ساب‌لینک معتبر نیست یا کاربر حذف شده است.</p>
        </div>
        </body>
        </html>
        """, status_code=404)
    
    active_connections_list = []
    for c in connections.values():
        if c.get("uuid") == uuid:
            active_connections_list.append(c)
    
    active_connections_count = len(active_connections_list)
    
    label = link.get("label", "کاربر")
    remark = f"عقاب-{label}"
    
    link_data = {
        **link,
        "expired": is_link_expired(link),
        "active_connections": active_connections_count,
        "active_connections_list": active_connections_list,
        "vless_link": generate_vless_link(
            uuid, 
            get_host(), 
            remark=remark,
            protocol=link.get("protocol", DEFAULT_PROTOCOL),
            fingerprint=link.get("fingerprint", "chrome"),
            port=link.get("port", 443)
        ),
        "sub_url": f"https://{get_host()}/sub/{uuid}",
    }
    
    return HTMLResponse(content=get_sub_page_html(uuid, link_data))

@app.get("/sub-all")
async def subscription_all(_=Depends(require_auth)):
    import base64
    host = get_host()
    async with LINKS_LOCK:
        lines = []
        for uid, d in LINKS.items():
            if is_link_allowed(d):
                fp = d.get("fingerprint", "chrome")
                port = d.get("port", 443)
                label = d.get("label", "کاربر")
                remark = f"عقاب-{label}"
                lines.append(generate_vless_link(uid, host, remark=remark, protocol=d.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=port))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")

    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")

    host = get_host()
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        lines = []
        for lid in link_ids:
            link = LINKS.get(lid)
            if link and is_link_allowed(link):
                fp = link.get("fingerprint", "chrome")
                port = link.get("port", 443)
                label = link.get("label", "کاربر")
                remark = f"عقاب-{label}"
                lines.append(generate_vless_link(lid, host, remark=remark, protocol=link.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=port))

    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "profile-title": quote(sub["name"]),
            "profile-update-interval": "12",
        }
    )

@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str):
    return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px;color:var(--t1)'>🦅 گروه اشتراک</h2>")

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="not found")
    sub_id, sub = sub_entry

    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})

    host = get_host()
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        snap = dict(LINKS)

    links_out = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        allowed = is_link_allowed(link)
        conn_count = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        proto = link.get("protocol", DEFAULT_PROTOCOL)
        fp = link.get("fingerprint", "chrome")
        port = link.get("port", 443)
        label = link.get("label", "کاربر")
        remark = f"عقاب-{label}"
        links_out.append({
            "uuid": lid,
            "label": link["label"],
            "active": allowed,
            "protocol": proto,
            "fingerprint": fp,
            "max_devices": link.get("max_devices", 0),
            "used_bytes": link.get("used_bytes", 0),
            "used_fmt": fmt_bytes(link.get("used_bytes", 0)),
            "limit_bytes": link.get("limit_bytes", 0),
            "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
            "expires_at": link.get("expires_at"),
            "has_password": link.get("password_hash") is not None,
            "port": port,
            "vless_link": generate_vless_link(lid, host, remark=remark, protocol=proto, fingerprint=fp, port=port),
            "sub_url": f"https://{host}/sub/{lid}",
            "connections": conn_count,
        })

    total_used = sum(l["used_bytes"] for l in links_out)
    return {
        "locked": False,
        "name": sub["name"],
        "desc": sub.get("desc", ""),
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
        "active_connections": active_conns,
        "total_used_fmt": fmt_bytes(total_used),
        "links": links_out,
    }

# ─── HTML Pages ─────────────────────────────────────────────────────────────

from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>🦅 Eagle Gateway</title>
    <style>
    body{font-family:sans-serif;background:#0a0a0f;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
    .card{text-align:center;padding:40px;background:rgba(20,20,40,0.7);border-radius:20px;border:1px solid rgba(255,80,20,0.2)}
    h1{font-size:48px;margin:0}
    .sub{color:#888}
    a{color:#FF6B35;text-decoration:none;font-weight:bold}
    </style>
    </head>
    <body>
    <div class="card">
        <h1>🦅</h1>
        <h2>Eagle Gateway v10 Pro</h2>
        <p class="sub">پنل مدیریت فیلترشکن</p>
        <a href="/login">ورود به پنل →</a>
    </div>
    </body>
    </html>
    """)

# ─── Run ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
