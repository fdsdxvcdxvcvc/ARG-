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

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Eagle-Gateway")

IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="🦅 Eagle Gateway", docs_url=None, redoc_url=None)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": os.environ.get("SECRET_KEY", secrets.token_urlsafe(32)),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Persistence ───────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "eagle_state.json"
SAVE_LOCK = asyncio.Lock()

async def load_state():
    global LINKS, AUTH, SUBS, SETTINGS, CLEAN_IPS, TELEGRAM_SETTINGS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            CLEAN_IPS.update(data.get("clean_ips", {}))
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            if "settings" in data:
                SETTINGS.update(data["settings"])
            if "telegram" in data:
                TELEGRAM_SETTINGS.update(data["telegram"])
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs, {len(CLEAN_IPS)} clean ips")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "clean_ips": dict(CLEAN_IPS),
                "password_hash": AUTH["password_hash"],
                "settings": SETTINGS,
                "telegram": TELEGRAM_SETTINGS,
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── In-memory state ───────────────────────────────────────────────────────────
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
http_client: httpx.AsyncClient | None = None
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()
SETTINGS: dict = {"rgb_mode": False}
CLEAN_IPS: dict = {}
CLEAN_IPS_LOCK = asyncio.Lock()
TELEGRAM_SETTINGS: dict = {
    "bot_token": "",
    "chat_id": "",
    "enabled": False,
    "webhook_set": False
}
TELEGRAM_LOCK = asyncio.Lock()

device_connections: dict = {}
DEVICE_CONNECTIONS_LOCK = asyncio.Lock()

PROTOCOLS = ("vless-ws", "xhttp-packet-up", "xhttp-stream-up", "xhttp-stream-one")
DEFAULT_PROTOCOL = "vless-ws"

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "eagle_session"
SESSION_TTL = 60 * 60 * 24 * 7

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "123456"))}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

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

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(
        limits=limits, timeout=timeout, follow_redirects=True,
    )
    await load_state()
    log_activity("system", "🦅 سرور راه‌اندازی شد", "ok")
    logger.info(f"🦅 Eagle Gateway started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client:
        await http_client.aclose()

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
    
def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def generate_vless_link(uuid: str, host: str, remark: str = "", protocol: str = DEFAULT_PROTOCOL, fingerprint: str = "chrome", port: int = 443, clean_ip: str = None) -> str:
    if not remark:
        remark = "عقاب"
    
    target_host = clean_ip if clean_ip else host
    target_port = port
    
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
    return f"vless://{uuid}@{target_host}:{target_port}?{query}#{quote(remark)}"

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
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

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

# ── Telegram Bot ──────────────────────────────────────────────────────────────

async def send_telegram_message(message: str) -> bool:
    """ارسال پیام به تلگرام"""
    if not TELEGRAM_SETTINGS.get("enabled", False):
        return False
    
    bot_token = TELEGRAM_SETTINGS.get("bot_token", "")
    chat_id = TELEGRAM_SETTINGS.get("chat_id", "")
    
    if not bot_token or not chat_id:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            })
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return False

async def telegram_bot_handler(update: dict):
    """پردازش دستورات ربات"""
    if "message" not in update:
        return
    
    message = update["message"]
    chat_id = str(message.get("chat", {}).get("id", ""))
    text = message.get("text", "").strip()
    from_user = message.get("from", {})
    username = from_user.get("username", "کاربر")
    
    if chat_id != TELEGRAM_SETTINGS.get("chat_id", ""):
        await send_telegram_message("⛔ شما دسترسی به این ربات ندارید!")
        return
    
    if text.startswith("/start"):
        await send_telegram_message("""🦅 <b>به ربات مدیریت پنل عقاب خوش آمدید!</b>

📋 <b>دستورات موجود:</b>

👤 <b>مدیریت کاربران:</b>
/create <نام> <حجم(GB)> <انقضا(روز)> - ساخت کاربر جدید
/list - لیست همه کاربران
/info <uuid> - اطلاعات کاربر
/reset <uuid> - ریست مصرف
/disable <uuid> - غیرفعال کردن
/enable <uuid> - فعال کردن
/delete <uuid> - حذف کاربر
/link <uuid> - دریافت لینک کانفیگ
/sublink <uuid> - دریافت ساب‌لینک

📊 <b>آمار و وضعیت:</b>
/stats - آمار کلی پنل
/online - کاربران آنلاین
/connections - اتصالات زنده

🔧 <b>تنظیمات:</b>
/botinfo - اطلاعات ربات

💡 مثال: 
/create علی 10 30""")

    elif text.startswith("/create"):
        parts = text.split()
        if len(parts) < 4:
            await send_telegram_message("❌ فرمت: /create <نام> <حجم(GB)> <انقضا(روز)>")
            return
        
        label = parts[1]
        try:
            quota = float(parts[2])
            exp_days = int(parts[3])
        except:
            await send_telegram_message("❌ حجم و انقضا باید عدد باشند!")
            return
        
        uid = generate_uuid()
        expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
        limit_bytes = int(quota * 1024 ** 3)
        
        async with LINKS_LOCK:
            LINKS[uid] = {
                "label": label,
                "limit_bytes": limit_bytes,
                "used_bytes": 0,
                "created_at": datetime.now().isoformat(),
                "active": True,
                "expires_at": expires_at,
                "note": f"ساخته شده توسط ربات @{username}",
                "is_default": False,
                "sub_id": None,
                "protocol": DEFAULT_PROTOCOL,
                "max_devices": 0,
                "fingerprint": "chrome",
                "password_hash": None,
                "port": 443,
            }
        
        await save_state()
        host = get_host()
        vless_link = generate_vless_link(uid, host, remark=f"عقاب-{label}")
        sub_url = f"https://{host}/sub/{uid}"
        
        await send_telegram_message(f"""✅ <b>کاربر با موفقیت ساخته شد!</b>

🆔 <b>UUID:</b> <code>{uid}</code>
👤 <b>نام:</b> {label}
📦 <b>حجم:</b> {quota} GB
📅 <b>انقضا:</b> {exp_days if exp_days > 0 else 'نامحدود'} روز

🔗 <b>لینک کانفیگ:</b>
<code>{vless_link}</code>

📎 <b>ساب‌لینک:</b>
{sub_url}

💡 برای مدیریت از دستورات استفاده کنید.""")
        log_activity("telegram", f"کاربر {label} توسط ربات ساخته شد", "ok")

    elif text.startswith("/list"):
        async with LINKS_LOCK:
            snap = dict(LINKS)
        
        if not snap:
            await send_telegram_message("📭 هیچ کاربری در پنل وجود ندارد!")
            return
        
        total = len(snap)
        online = sum(1 for l in snap.values() if l.get("active", True) and not is_link_expired(l))
        
        msg = f"📋 <b>لیست کاربران ({total} کاربر)</b>\n\n"
        for uid, link in list(snap.items())[:20]:
            status = "🟢" if link.get("active", True) and not is_link_expired(link) else "🔴"
            used = fmt_bytes(link.get("used_bytes", 0))
            label = link.get("label", "نامشخص")
            msg += f"{status} <b>{label}</b>\n  <code>{uid[:8]}...{uid[-8:]}</code> | مصرف: {used}\n"
        
        if len(snap) > 20:
            msg += f"\n... و {len(snap)-20} کاربر دیگر"
        
        msg += f"\n\n🟢 آنلاین: {online} | 📊 کل مصرف: {fmt_bytes(sum(l.get('used_bytes', 0) for l in snap.values()))}"
        await send_telegram_message(msg)

    elif text.startswith("/info"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /info <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            link = LINKS.get(uid)
        
        if not link:
            await send_telegram_message(f"❌ کاربر با UUID <code>{uid}</code> یافت نشد!")
            return
        
        label = link.get("label", "نامشخص")
        used = fmt_bytes(link.get("used_bytes", 0))
        limit = fmt_bytes(link.get("limit_bytes", 0)) if link.get("limit_bytes", 0) > 0 else "∞"
        active = "✅ فعال" if link.get("active", True) and not is_link_expired(link) else "❌ غیرفعال"
        created = link.get("created_at", "نامشخص")[:10]
        
        msg = f"""📋 <b>اطلاعات کاربر</b>

👤 <b>نام:</b> {label}
🆔 <b>UUID:</b> <code>{uid}</code>
📊 <b>مصرف:</b> {used} / {limit}
📅 <b>تاریخ ساخت:</b> {created}
🔴 <b>وضعیت:</b> {active}
📱 <b>دستگاه‌ها:</b> {link.get('max_devices', 0) if link.get('max_devices', 0) > 0 else '∞'}
🔌 <b>پروتکل:</b> {link.get('protocol', DEFAULT_PROTOCOL)}"""
        
        conns = [c for c in connections.values() if c.get("uuid") == uid]
        if conns:
            msg += f"\n\n🔌 <b>اتصالات زنده:</b> {len(conns)}"
            for c in conns[:5]:
                msg += f"\n  • {c.get('ip', 'نامشخص')}"
            if len(conns) > 5:
                msg += f"\n  ... و {len(conns)-5} اتصال دیگر"
        
        await send_telegram_message(msg)

    elif text.startswith("/reset"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /reset <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            if uid not in LINKS:
                await send_telegram_message(f"❌ کاربر یافت نشد!")
                return
            LINKS[uid]["used_bytes"] = 0
        
        await save_state()
        await send_telegram_message(f"✅ مصرف کاربر <code>{uid}</code> ریست شد!")

    elif text.startswith("/disable"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /disable <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            if uid not in LINKS:
                await send_telegram_message(f"❌ کاربر یافت نشد!")
                return
            LINKS[uid]["active"] = False
        
        await save_state()
        await send_telegram_message(f"⛔ کاربر <code>{uid}</code> غیرفعال شد!")

    elif text.startswith("/enable"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /enable <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            if uid not in LINKS:
                await send_telegram_message(f"❌ کاربر یافت نشد!")
                return
            LINKS[uid]["active"] = True
        
        await save_state()
        await send_telegram_message(f"✅ کاربر <code>{uid}</code> فعال شد!")

    elif text.startswith("/delete"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /delete <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            if uid not in LINKS:
                await send_telegram_message(f"❌ کاربر یافت نشد!")
                return
            label = LINKS[uid].get("label", uid)
            del LINKS[uid]
        
        async with CLEAN_IPS_LOCK:
            if uid in CLEAN_IPS:
                del CLEAN_IPS[uid]
        
        await save_state()
        await send_telegram_message(f"🗑️ کاربر <b>{label}</b> (<code>{uid}</code>) حذف شد!")

    elif text.startswith("/link"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /link <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            link = LINKS.get(uid)
        
        if not link:
            await send_telegram_message(f"❌ کاربر یافت نشد!")
            return
        
        host = get_host()
        label = link.get("label", "کاربر")
        vless_link = generate_vless_link(uid, host, remark=f"عقاب-{label}")
        await send_telegram_message(f"🔗 <b>لینک کانفیگ</b>\n\n<code>{vless_link}</code>")

    elif text.startswith("/sublink"):
        parts = text.split()
        if len(parts) < 2:
            await send_telegram_message("❌ UUID را وارد کنید: /sublink <uuid>")
            return
        
        uid = parts[1]
        async with LINKS_LOCK:
            if uid not in LINKS:
                await send_telegram_message(f"❌ کاربر یافت نشد!")
                return
        
        host = get_host()
        sub_url = f"https://{host}/sub/{uid}"
        await send_telegram_message(f"📎 <b>ساب‌لینک</b>\n\n<code>{sub_url}</code>")

    elif text.startswith("/stats"):
        async with LINKS_LOCK:
            snap = dict(LINKS)
        
        total_users = len(snap)
        active_users = sum(1 for l in snap.values() if l.get("active", True) and not is_link_expired(l))
        total_used = sum(l.get("used_bytes", 0) for l in snap.values())
        total_limit = sum(l.get("limit_bytes", 0) for l in snap.values())
        online_conns = len(connections)
        
        msg = f"""📊 <b>آمار کلی پنل</b>

👥 <b>کل کاربران:</b> {total_users}
🟢 <b>کاربران فعال:</b> {active_users}
🔴 <b>کاربران غیرفعال:</b> {total_users - active_users}
📊 <b>مصرف کل:</b> {fmt_bytes(total_used)}
📦 <b>سهمیه کل:</b> {fmt_bytes(total_limit)}
🔌 <b>اتصالات زنده:</b> {online_conns}
⏱️ <b>آپتایم:</b> {uptime()}
📅 <b>تاریخ:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        await send_telegram_message(msg)

    elif text.startswith("/online"):
        if not connections:
            await send_telegram_message("🔴 هیچ کاربری آنلاین نیست!")
            return
        
        async with LINKS_LOCK:
            snap = dict(LINKS)
        
        online_users = {}
        for c in connections.values():
            uid = c.get("uuid")
            if uid:
                if uid not in online_users:
                    online_users[uid] = []
                online_users[uid].append(c)
        
        if not online_users:
            await send_telegram_message("🔴 هیچ کاربری آنلاین نیست!")
            return
        
        msg = f"🟢 <b>کاربران آنلاین ({len(online_users)} کاربر)</b>\n\n"
        for uid, conns in list(online_users.items())[:15]:
            link = snap.get(uid, {})
            label = link.get("label", "نامشخص")
            msg += f"👤 <b>{label}</b> | {len(conns)} اتصال\n"
        
        if len(online_users) > 15:
            msg += f"\n... و {len(online_users)-15} کاربر دیگر"
        
        await send_telegram_message(msg)

    elif text.startswith("/connections"):
        if not connections:
            await send_telegram_message("🔴 هیچ اتصال فعالی وجود ندارد!")
            return
        
        async with LINKS_LOCK:
            snap = dict(LINKS)
        
        msg = f"🔌 <b>اتصالات زنده ({len(connections)} اتصال)</b>\n\n"
        for i, (conn_id, c) in enumerate(list(connections.items())[:10], 1):
            ip = c.get("ip", "نامشخص")
            uid = c.get("uuid", "نامشخص")
            link = snap.get(uid, {})
            label = link.get("label", "نامشخص")
            msg += f"{i}. {ip} - <b>{label}</b>\n"
        
        if len(connections) > 10:
            msg += f"\n... و {len(connections)-10} اتصال دیگر"
        
        await send_telegram_message(msg)

    elif text.startswith("/botinfo"):
        enabled = TELEGRAM_SETTINGS.get("enabled", False)
        token = TELEGRAM_SETTINGS.get("bot_token", "")
        chat_id = TELEGRAM_SETTINGS.get("chat_id", "")
        
        msg = f"""🤖 <b>اطلاعات ربات</b>

📌 <b>وضعیت:</b> {'✅ فعال' if enabled else '❌ غیرفعال'}
🔑 <b>Token:</b> {'***' + token[-6:] if token else 'تنظیم نشده'}
💬 <b>Chat ID:</b> {chat_id if chat_id else 'تنظیم نشده'}
📎 <b>Webhook:</b> {'✅ تنظیم شده' if TELEGRAM_SETTINGS.get('webhook_set') else '❌ تنظیم نشده'}

📋 <b>دستورات موجود:</b>
/start - راهنما
/create - ساخت کاربر
/list - لیست کاربران
/info - اطلاعات کاربر
/reset - ریست مصرف
/disable - غیرفعال کردن
/enable - فعال کردن
/delete - حذف کاربر
/link - دریافت لینک
/sublink - دریافت ساب‌لینک
/stats - آمار پنل
/online - کاربران آنلاین
/connections - اتصالات زنده
/botinfo - اطلاعات ربات"""
        
        await send_telegram_message(msg)

    else:
        await send_telegram_message(f"""❌ دستور <code>{text}</code> شناسایی نشد!

📋 برای مشاهده راهنما، دستور /start را وارد کنید.""")

# ── Webhook برای ربات تلگرام ───────────────────────────────────────────────
@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        asyncio.create_task(telegram_bot_handler(update))
        return {"ok": True}
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return {"ok": False}

# ── API برای تنظیمات ربات ──────────────────────────────────────────────────
@app.post("/api/telegram/settings")
async def set_telegram_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    bot_token = body.get("bot_token", "").strip()
    chat_id = body.get("chat_id", "").strip()
    enabled = body.get("enabled", False)
    
    if bot_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    raise HTTPException(status_code=400, detail="توکن ربات نامعتبر است")
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json={
                    "chat_id": chat_id,
                    "text": "🦅 پنل عقاب با موفقیت به ربات متصل شد!"
                })
                if resp.status_code != 200:
                    raise HTTPException(status_code=400, detail="چت آیدی نامعتبر است")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"خطا در اتصال به ربات: {str(e)}")
    
    TELEGRAM_SETTINGS["bot_token"] = bot_token
    TELEGRAM_SETTINGS["chat_id"] = chat_id
    TELEGRAM_SETTINGS["enabled"] = enabled
    
    await save_state()
    log_activity("telegram", f"تنظیمات ربات {'فعال' if enabled else 'غیرفعال'} شد", "ok")
    return {"ok": True, "settings": TELEGRAM_SETTINGS}

@app.get("/api/telegram/settings")
async def get_telegram_settings(_=Depends(require_auth)):
    return {
        "bot_token": TELEGRAM_SETTINGS.get("bot_token", ""),
        "chat_id": TELEGRAM_SETTINGS.get("chat_id", ""),
        "enabled": TELEGRAM_SETTINGS.get("enabled", False),
        "webhook_set": TELEGRAM_SETTINGS.get("webhook_set", False),
        "webhook_url": f"https://{get_host()}/webhook/telegram"
    }

@app.post("/api/telegram/set-webhook")
async def set_telegram_webhook(_=Depends(require_auth)):
    bot_token = TELEGRAM_SETTINGS.get("bot_token", "")
    if not bot_token:
        raise HTTPException(status_code=400, detail="توکن ربات تنظیم نشده است")
    
    webhook_url = f"https://{get_host()}/webhook/telegram"
    try:
        url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json={"url": webhook_url})
            data = resp.json()
            if data.get("ok"):
                TELEGRAM_SETTINGS["webhook_set"] = True
                await save_state()
                return {"ok": True, "webhook_url": webhook_url}
            else:
                raise HTTPException(status_code=400, detail=data.get("description", "خطا در تنظیم webhook"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"خطا: {str(e)}")

# ── Settings API ──────────────────────────────────────────────────────────────
@app.get("/api/settings")
async def get_settings(_=Depends(require_auth)):
    return SETTINGS

@app.post("/api/settings/rgb")
async def toggle_rgb(request: Request, _=Depends(require_auth)):
    body = await request.json()
    SETTINGS["rgb_mode"] = bool(body.get("enabled", False))
    await save_state()
    return {"rgb_mode": SETTINGS["rgb_mode"]}

# ── Change Password ──────────────────────────────────────────────────────────
@app.post("/api/change-password")
async def change_password(request: Request, _=Depends(require_auth)):
    body = await request.json()
    current_password = body.get("current_password", "").strip()
    new_password = body.get("new_password", "").strip()
    confirm_password = body.get("confirm_password", "").strip()
    
    if hash_password(current_password) != AUTH["password_hash"]:
        raise HTTPException(status_code=403, detail="رمز فعلی اشتباه است")
    
    if len(new_password) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="رمز جدید و تکرار آن مطابقت ندارند")
    
    AUTH["password_hash"] = hash_password(new_password)
    await save_state()
    
    async with SESSIONS_LOCK:
        SESSIONS.clear()
    
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True, "message": "رمز عبور با موفقیت تغییر کرد"}

# ── Default link ──────────────────────────────────────────────────────────────
_default_link_created = False

async def ensure_default_link():
    global _default_link_created
    if _default_link_created:
        return
    async with LINKS_LOCK:
        if not any(l.get("is_default") for l in LINKS.values()):
            uid = hashlib.sha256(f"default{CONFIG['secret']}".encode()).hexdigest()
            uid = f"{uid[:8]}-{uid[8:12]}-{uid[12:16]}-{uid[16:20]}-{uid[20:32]}"
            if uid not in LINKS:
                LINKS[uid] = {
                    "label": "لینک پیش‌فرض",
                    "limit_bytes": 0,
                    "used_bytes": 0,
                    "created_at": datetime.now().isoformat(),
                    "active": True,
                    "expires_at": None,
                    "note": "",
                    "is_default": True,
                    "sub_id": None,
                    "protocol": DEFAULT_PROTOCOL,
                    "max_devices": 0,
                    "fingerprint": "chrome",
                    "password_hash": None,
                    "port": 443,
                }
                asyncio.create_task(save_state())
        _default_link_created = True

# ── Basic endpoints ───────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"service": "🦅 Eagle Gateway", "version": "10.0", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}

# ── Clean IPs API ────────────────────────────────────────────────────────────
@app.post("/api/links/{uid}/clean-ips")
async def add_clean_ips(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    ips = body.get("ips", [])
    
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
    
    added = []
    async with CLEAN_IPS_LOCK:
        if uid not in CLEAN_IPS:
            CLEAN_IPS[uid] = []
        
        for ip_str in ips:
            ip_str = ip_str.strip()
            if not ip_str:
                continue
            
            if ":" in ip_str:
                parts = ip_str.split(":")
                ip_addr = parts[0].strip()
                try:
                    port = int(parts[1].strip()) if len(parts) > 1 else 443
                except:
                    port = 443
            else:
                ip_addr = ip_str
                port = 443
            
            if not any(x["ip"] == ip_addr and x["port"] == port for x in CLEAN_IPS[uid]):
                CLEAN_IPS[uid].append({"ip": ip_addr, "port": port, "active": True})
                added.append({"ip": ip_addr, "port": port})
    
    await save_state()
    return {"ok": True, "added": added, "ips": CLEAN_IPS.get(uid, [])}

@app.delete("/api/links/{uid}/clean-ips")
async def remove_clean_ip(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    ip = body.get("ip", "")
    port = body.get("port", 443)
    
    async with CLEAN_IPS_LOCK:
        if uid in CLEAN_IPS:
            CLEAN_IPS[uid] = [x for x in CLEAN_IPS[uid] if not (x["ip"] == ip and x["port"] == port)]
    
    await save_state()
    return {"ok": True}

@app.get("/api/links/{uid}/clean-ips")
async def get_clean_ips(uid: str, _=Depends(require_auth)):
    async with CLEAN_IPS_LOCK:
        return {"ips": CLEAN_IPS.get(uid, [])}

# ── Subscription ──────────────────────────────────────────────────────────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str):
    from pages import get_sub_page_html
    
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    
    if not link:
        return HTMLResponse("""<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>🦅 کاربر یافت نشد</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;800&display=swap" rel="stylesheet"><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Vazirmatn',sans-serif;background:#0a0a0f;min-height:100vh;display:flex;align-items:center;justify-content:center;color:#F0F0FF}.card{background:rgba(15,15,30,0.85);backdrop-filter:blur(30px);border:1px solid rgba(59,130,246,0.12);border-radius:28px;padding:40px;max-width:420px;text-align:center}.icon{font-size:64px;margin-bottom:16px}h2{font-size:22px;font-weight:800;margin-bottom:8px}p{color:#6A6A8A;font-size:13px;line-height:1.8}</style></head><body><div class="card"><div class="icon">🦅</div><h2>کاربر یافت نشد</h2><p>لینک ساب‌لینک معتبر نیست یا کاربر حذف شده است.</p></div></body></html>""", status_code=404)
    
    active_connections_list = [c for c in connections.values() if c.get("uuid") == uuid]
    active_connections_count = len(active_connections_list)
    
    label = link.get("label", "کاربر")
    remark = f"عقاب-{label}"
    
    async with CLEAN_IPS_LOCK:
        clean_ips = CLEAN_IPS.get(uuid, [])
    
    link_data = {
        **link,
        "expired": is_link_expired(link),
        "active_connections": active_connections_count,
        "active_connections_list": active_connections_list,
        "clean_ips": clean_ips,
        "vless_link": generate_vless_link(uuid, get_host(), remark=remark, protocol=link.get("protocol", DEFAULT_PROTOCOL), fingerprint=link.get("fingerprint", "chrome"), port=link.get("port", 443)),
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
                
                async with CLEAN_IPS_LOCK:
                    clean_ips = CLEAN_IPS.get(uid, [])
                
                if clean_ips:
                    for ci in clean_ips:
                        if ci.get("active", True):
                            lines.append(generate_vless_link(uid, host, remark=remark, protocol=d.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=ci.get("port", port), clean_ip=ci["ip"]))
                else:
                    lines.append(generate_vless_link(uid, host, remark=remark, protocol=d.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=port))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

# ── Sub Groups ─────────────────────────────────────────────────────────────────
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
    return {"ok": True, "deleted": sub_id}

@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    link_id = str(body.get("link_id", ""))
    action = str(body.get("action", "add"))
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        ids = s.setdefault("link_ids", [])
        if action == "add":
            if link_id not in ids:
                ids.append(link_id)
        else:
            if link_id in ids:
                ids.remove(link_id)
    async with LINKS_LOCK:
        if link_id in LINKS:
            LINKS[link_id]["sub_id"] = sub_id if action == "add" else None
    asyncio.create_task(save_state())
    return {"ok": True}

# ── Public sub-group subscription ────────────────────────────────────────────
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
                
                async with CLEAN_IPS_LOCK:
                    clean_ips = CLEAN_IPS.get(lid, [])
                
                if clean_ips:
                    for ci in clean_ips:
                        if ci.get("active", True):
                            lines.append(generate_vless_link(lid, host, remark=remark, protocol=link.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=ci.get("port", port), clean_ip=ci["ip"]))
                else:
                    lines.append(generate_vless_link(lid, host, remark=remark, protocol=link.get("protocol", DEFAULT_PROTOCOL), fingerprint=fp, port=port))

    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain", headers={"profile-title": quote(sub["name"]), "profile-update-interval": "12"})

# ── Auth endpoints ────────────────────────────────────────────────────────────
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

# ── Stats ─────────────────────────────────────────────────────────────────────
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
            top_user = {"uuid": uid, "label": link.get("label", "نامشخص"), "used_bytes": used, "used_fmt": fmt_bytes(used)}
    
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

# ── Live connections ──────────────────────────────────────────────────────────
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
            g = {"ip": ip, "sessions": 0, "bytes": 0, "labels": set(), "transports": set(), "first_connected_at": c.get("connected_at"), "last_connected_at": c.get("connected_at")}
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
        result.append({"ip": ip, "sessions": g["sessions"], "labels": sorted(g["labels"]), "label": " · ".join(sorted(g["labels"])) if g["labels"] else "نامشخص", "transports": sorted(g["transports"]), "bytes": g["bytes"], "bytes_fmt": fmt_bytes(g["bytes"]), "connected_at": g["first_connected_at"], "last_connected_at": g["last_connected_at"]})
    result.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)

    return {"connections": result, "count": len(result), "raw_count": len(connections)}

# ── Link Management ───────────────────────────────────────────────────────────
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
    
    return {
        "uuid": uid,
        **LINKS[uid],
        "expired": False,
        "has_password": password_hash is not None,
        "vless_link": main_link,
        "warning_config": "",
        "sub_url": f"https://{host}/sub/{uid}",
    }

@app.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = get_host()
    async with LINKS_LOCK:
        snap = dict(LINKS)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_usage = {}
    for uid, d in snap.items():
        today_usage[uid] = d.get("used_bytes", 0)
    
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
        
        active = d.get("active", True) and not is_link_expired(d)
        status_text = "🟢 آنلاین" if active else "🔴 آفلاین"
        status_class = "on" if active else "off"
        
        async with CLEAN_IPS_LOCK:
            clean_ips = CLEAN_IPS.get(uid, [])
        
        result.append({
            "uuid": uid,
            **d,
            "protocol": proto,
            "fingerprint": fp,
            "max_devices": d.get("max_devices", 0),
            "expired": is_link_expired(d),
            "has_password": d.get("password_hash") is not None,
            "port": port,
            "today_bytes": today_usage.get(uid, 0),
            "last_connected_at": last_connected,
            "status_text": status_text,
            "status_class": status_class,
            "vless_link": generate_vless_link(uid, host, remark=remark, protocol=proto, fingerprint=fp, port=port),
            "warning_config": "",
            "sub_url": f"https://{host}/sub/{uid}",
            "clean_ips": clean_ips,
            "clean_ips_count": len(clean_ips),
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
        if "protocol" in body:
            protocol = body["protocol"]
            if protocol in PROTOCOLS:
                link["protocol"] = protocol
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
    
    async with CLEAN_IPS_LOCK:
        if uid in CLEAN_IPS:
            del CLEAN_IPS[uid]
    
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    
    asyncio.create_task(save_state())
    return {"ok": True, "deleted": uid}

# ══════════════════════════════════════════════════════════════════════════════
# VLESS Relay
# ══════════════════════════════════════════════════════════════════════════════

async def patched_check_and_use(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] = link.get("used_bytes", 0) + n
        stats["total_bytes"] = stats.get("total_bytes", 0) + n
        hourly_traffic[now_ir().strftime("%H:00")] = hourly_traffic.get(now_ir().strftime("%H:00"), 0) + n
    return True

try:
    from relay_vless import (
        RELAY_BUF,
        parse_vless_header,
        relay_ws_to_tcp,
        relay_tcp_to_ws,
        websocket_tunnel,
    )
    app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)
except ImportError:
    logger.warning("relay_vless not found, WebSocket relay disabled")

# ══════════════════════════════════════════════════════════════════════════════
# XHTTP
# ══════════════════════════════════════════════════════════════════════════════
try:
    from xhttp_siz10 import router as xhttp_router
    app.include_router(xhttp_router)
except:
    pass

# ── HTTP Proxy ────────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        hourly_traffic[now_ir().strftime("%H:00")] += len(resp.content)
        return Response(content=resp.content, status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── Public sub page ───────────────────────────────────────────────────────────
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
        
        async with CLEAN_IPS_LOCK:
            clean_ips = CLEAN_IPS.get(lid, [])
        
        vless_links = []
        if clean_ips:
            for ci in clean_ips:
                if ci.get("active", True):
                    vless_links.append(generate_vless_link(lid, host, remark=remark, protocol=proto, fingerprint=fp, port=ci.get("port", port), clean_ip=ci["ip"]))
        else:
            vless_links.append(generate_vless_link(lid, host, remark=remark, protocol=proto, fingerprint=fp, port=port))
        
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
            "vless_links": vless_links,
            "vless_link": vless_links[0] if vless_links else "",
            "clean_ips_count": len(clean_ips),
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

# ── HTML Pages ────────────────────────────────────────────────────────────────
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
    await ensure_default_link()
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/test-ws", response_class=HTMLResponse)
async def test_ws_redirect():
    return HTMLResponse(content="<script>location.href='/dashboard'</script>")

# ── Backup ────────────────────────────────────────────────────────────────────
@app.get("/api/backup")
async def get_backup(_=Depends(require_auth)):
    async with LINKS_LOCK:
        links = dict(LINKS)
    async with SUBS_LOCK:
        subs = dict(SUBS)
    async with CLEAN_IPS_LOCK:
        clean_ips = dict(CLEAN_IPS)
    return {
        "links": links,
        "subs": subs,
        "clean_ips": clean_ips,
        "password_hash": AUTH["password_hash"],
        "settings": SETTINGS,
        "telegram": TELEGRAM_SETTINGS,
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
        
        if "clean_ips" in body and isinstance(body["clean_ips"], dict):
            async with CLEAN_IPS_LOCK:
                CLEAN_IPS.clear()
                for uid, ips in body["clean_ips"].items():
                    if isinstance(ips, list):
                        CLEAN_IPS[uid] = ips
        
        if "password_hash" in body:
            AUTH["password_hash"] = body["password_hash"]
        
        if "settings" in body and isinstance(body["settings"], dict):
            SETTINGS.update(body["settings"])
        
        if "telegram" in body and isinstance(body["telegram"], dict):
            TELEGRAM_SETTINGS.update(body["telegram"])
        
        await save_state()
        log_activity("backup", "بکاپ بازیابی شد", "ok")
        return {"ok": True, "message": "بکاپ با موفقیت بازیابی شد"}
    except Exception as e:
        logger.error(f"Backup restore error: {e}")
        raise HTTPException(status_code=400, detail=f"خطا در بازیابی بکاپ: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
