# relay_vless.py - WebSocket to TCP relay برای VLESS
# نسخه کامل و هماهنگ با پنل عقاب

import asyncio
import json
import logging
import time
import uuid as uuid_lib
from fastapi import WebSocket, WebSocketDisconnect
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger("Eagle-Gateway")

RELAY_BUF = 8192
CONNECTION_TIMEOUT = 30

# ── اتصالات فعال ─────────────────────────────────────────────────────────────
# این دیکشنری توسط main.py مدیریت میشه، ولی برای دسترسی راحت تعریفش میکنیم
connections = {}

# ── توابع کمکی ──────────────────────────────────────────────────────────────

def get_uuid_from_bytes(data: bytes) -> str | None:
    """استخراج UUID از هدر VLESS"""
    try:
        if len(data) < 17:
            return None
        uuid_bytes = data[1:17]
        uid = str(uuid_lib.UUID(bytes=uuid_bytes))
        return uid
    except Exception as e:
        logger.debug(f"UUID extraction failed: {e}")
        return None

async def parse_vless_header(data: bytes) -> dict:
    """پارسه هدر VLESS و استخراج UUID و داده باقیمانده"""
    try:
        if len(data) < 17:
            return None
        
        uid = get_uuid_from_bytes(data)
        if not uid:
            return None
        
        return {
            "uuid": uid,
            "data": data[17:] if len(data) > 17 else b""
        }
    except Exception as e:
        logger.error(f"VLESS header parse error: {e}")
        return None

# ── Relay functions ──────────────────────────────────────────────────────────

async def relay_ws_to_tcp(websocket: WebSocket, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, conn_id: str = None):
    """پخش داده از WebSocket به TCP"""
    try:
        while True:
            data = await websocket.receive_bytes()
            if not data:
                break
            
            # به‌روزرسانی آمار
            if conn_id and conn_id in connections:
                connections[conn_id]["bytes"] = connections[conn_id].get("bytes", 0) + len(data)
            
            writer.write(data)
            await writer.drain()
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.debug(f"WS->TCP relay error: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def relay_tcp_to_ws(websocket: WebSocket, reader: asyncio.StreamReader, conn_id: str = None):
    """پخش داده از TCP به WebSocket"""
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            
            # به‌روزرسانی آمار
            if conn_id and conn_id in connections:
                connections[conn_id]["bytes"] = connections[conn_id].get("bytes", 0) + len(data)
            
            await websocket.send_bytes(data)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.debug(f"TCP->WS relay error: {e}")

# ── تابع اصلی WebSocket Tunnel ─────────────────────────────────────────────

async def websocket_tunnel(websocket: WebSocket, uuid: str):
    """تونل WebSocket برای VLESS - نقطه ورود اصلی"""
    global connections
    
    # دریافت IP کلاینت
    client_ip = websocket.client.host if websocket.client else "نامشخص"
    conn_id = f"{uuid}_{client_ip}_{int(time.time()*1000)}"
    
    logger.info(f"🟢 WebSocket connection: {uuid} from {client_ip}")
    
    # دریافت دیکشنری‌های گلوبال از main
    try:
        from main import LINKS, LINKS_LOCK, is_link_allowed
    except ImportError:
        logger.error("Cannot import from main")
        await websocket.close(code=1011)
        return
    
    # ثبت اتصال
    connections[conn_id] = {
        "uuid": uuid,
        "ip": client_ip,
        "connected_at": time.time(),
        "bytes": 0,
        "transport": "vless-ws",
        "active": True
    }
    
    try:
        # قبول اتصال WebSocket
        await websocket.accept()
        
        # بررسی مجاز بودن کاربر
        async with LINKS_LOCK:
            link = LINKS.get(uuid)
            if not link:
                logger.warning(f"❌ UUID not found: {uuid}")
                await websocket.send_text(json.dumps({"error": "user not found"}))
                await websocket.close(code=1008)
                return
            
            if not is_link_allowed(link):
                logger.warning(f"❌ User not allowed: {uuid}")
                await websocket.send_text(json.dumps({"error": "user not allowed"}))
                await websocket.close(code=1008)
                return
        
        # دریافت اولین بسته
        try:
            first_data = await asyncio.wait_for(websocket.receive_bytes(), timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning(f"⏱️ Timeout waiting for data from {uuid}")
            await websocket.close(code=1008)
            return
        
        # پارس هدر VLESS
        header = await parse_vless_header(first_data)
        if not header:
            logger.warning(f"❌ Invalid VLESS header from {uuid}")
            await websocket.close(code=1008)
            return
        
        # بررسی اینکه UUID داخل هدر با UUID درخواستی یکی باشه
        if header.get("uuid") != uuid:
            logger.warning(f"❌ UUID mismatch: {header.get('uuid')} != {uuid}")
            await websocket.close(code=1008)
            return
        
        # ── اتصال به سرور مقصد ──────────────────────────────────────────
        # اینجا آدرس سرور واقعی رو تنظیم کن
        # میتونه آدرس IP سرور، یا 127.0.0.1 باشه
        
        # گزینه ۱: استفاده از تنظیمات محیطی
        target_host = os.environ.get("TARGET_HOST", "127.0.0.1")
        target_port = int(os.environ.get("TARGET_PORT", 443))
        
        # گزینه ۲: استفاده از آدرس خود پنل (برای تست)
        # target_host = "127.0.0.1"
        # target_port = 443
        
        # گزینه ۳: استفاده از آدرس دامنه پنل
        # from main import get_host
        # target_host = get_host()
        # target_port = 443
        
        logger.info(f"🔗 Connecting to {target_host}:{target_port}")
        
        try:
            reader, writer = await asyncio.open_connection(target_host, target_port)
        except Exception as e:
            logger.error(f"❌ TCP connection failed to {target_host}:{target_port} - {e}")
            await websocket.send_text(json.dumps({"error": f"connection failed: {e}"}))
            await websocket.close(code=1011)
            return
        
        # ارسال داده باقیمانده از هدر
        remaining = header.get("data", b"")
        if remaining:
            writer.write(remaining)
            await writer.drain()
        
        # ── شروع Relay ──────────────────────────────────────────────────
        logger.info(f"✅ Tunnel established for {uuid} ({client_ip})")
        
        # ایجاد تسک‌های relay
        ws_task = asyncio.create_task(relay_ws_to_tcp(websocket, reader, writer, conn_id))
        tcp_task = asyncio.create_task(relay_tcp_to_ws(websocket, reader, conn_id))
        
        # منتظر موندن تا یکی از تسک‌ها تموم بشه
        done, pending = await asyncio.wait(
            [ws_task, tcp_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # لغو تسک باقیمانده
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"🔴 Tunnel closed for {uuid} ({client_ip})")
        
    except WebSocketDisconnect:
        logger.info(f"🔴 WebSocket disconnected: {uuid} ({client_ip})")
    except Exception as e:
        logger.error(f"❌ WebSocket tunnel error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # پاک کردن اتصال
        if conn_id in connections:
            del connections[conn_id]
        
        try:
            await websocket.close()
        except:
            pass

# ── تابع جایگزین برای WS (در صورت نیاز) ──────────────────────────────────

async def ws_handler(websocket: WebSocket, uuid: str):
    """Handler ساده برای WebSocket"""
    await websocket_tunnel(websocket, uuid)

# ── صادرات ──────────────────────────────────────────────────────────────────

__all__ = [
    'RELAY_BUF',
    'connections',
    'parse_vless_header',
    'relay_ws_to_tcp',
    'relay_tcp_to_ws',
    'websocket_tunnel',
    'ws_handler',
]
