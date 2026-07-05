# relay_vless.py - با خطاگیری کامل

import asyncio
import socket
import logging
from datetime import datetime

logger = logging.getLogger("ARG-Gateway")
RELAY_BUF = 64 * 1024

# ===== تنظیمات Xray =====
XRAY_HOST = "127.0.0.1"
XRAY_PORT = 443  # ← اگه پورت Xray فرق داره، اینو تغییر بده

async def relay_ws_to_tcp(websocket, sock, uuid):
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_bytes(), timeout=30.0)
                if not data:
                    break
                sock.sendall(data)
            except asyncio.TimeoutError:
                continue
            except:
                break
    except:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

async def relay_tcp_to_ws(websocket, sock, uuid):
    loop = asyncio.get_event_loop()
    try:
        while True:
            try:
                data = await asyncio.wait_for(loop.sock_recv(sock, RELAY_BUF), timeout=30.0)
                if not data:
                    break
                await websocket.send_bytes(data)
            except asyncio.TimeoutError:
                continue
            except:
                break
    except:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

async def websocket_tunnel(websocket, uuid):
    from main import connections, LINKS, LINKS_LOCK, log_activity, is_link_allowed
    
    client_addr = websocket.client.host if websocket.client else "unknown"
    logger.info(f"🔗 New connection: {uuid} from {client_addr}")
    
    # بررسی اعتبار کاربر
    try:
        async with LINKS_LOCK:
            link = LINKS.get(uuid)
            if not link:
                await websocket.close(code=1008, reason="User not found")
                logger.warning(f"❌ User not found: {uuid}")
                return
            if not is_link_allowed(link):
                await websocket.close(code=1008, reason="User inactive")
                logger.warning(f"❌ User inactive: {uuid}")
                return
            logger.info(f"✅ User validated: {uuid}")
    except Exception as e:
        logger.error(f"❌ Auth error: {e}")
        await websocket.close(code=1011)
        return
    
    sock = None
    try:
        # ===== اتصال به Xray =====
        logger.info(f"🔗 Connecting to Xray: {XRAY_HOST}:{XRAY_PORT}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((XRAY_HOST, XRAY_PORT))
        sock.settimeout(None)
        logger.info(f"✅ Connected to Xray: {XRAY_HOST}:{XRAY_PORT}")
        
        connections[uuid] = {
            "ip": client_addr,
            "uuid": uuid,
            "connected_at": datetime.now().isoformat(),
            "transport": "vless-ws"
        }
        
        await asyncio.gather(
            relay_ws_to_tcp(websocket, sock, uuid),
            relay_tcp_to_ws(websocket, sock, uuid)
        )
        
    except ConnectionRefusedError:
        logger.error(f"🚫 Xray is NOT running on {XRAY_HOST}:{XRAY_PORT}")
        logger.error("💡 Please install and start Xray first!")
        await websocket.close(code=1011, reason="Xray not running")
        
    except socket.timeout:
        logger.error(f"⏱️ Connection timeout to Xray: {XRAY_HOST}:{XRAY_PORT}")
        await websocket.close(code=1011, reason="Connection timeout")
        
    except Exception as e:
        logger.error(f"❌ WS error: {e}")
        await websocket.close(code=1011, reason=f"Error: {str(e)[:50]}")
        
    finally:
        connections.pop(uuid, None)
        if sock:
            try:
                sock.close()
            except:
                pass
        try:
            await websocket.close()
        except:
            pass
        logger.info(f"👋 Disconnected: {uuid}")
