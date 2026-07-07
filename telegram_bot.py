# telegram_bot.py - ربات کامل مدیریت پنل عقاب 🦅

import asyncio
import json
import os
import logging
import httpx
from datetime import datetime, timedelta
from typing import Dict, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ─── تنظیمات ──────────────────────────────────────────────────────────────────
PANEL_URL = os.environ.get("PANEL_URL", "http://localhost:8000")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "123456")
ALLOWED_USERS = os.environ.get("ALLOWED_USERS", "").split(",")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Eagle-Bot")

if not TELEGRAM_BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN تنظیم نشده!")
    exit(1)

# ─── دیتا ─────────────────────────────────────────────────────────────────────
pending_actions = {}
panel_session = {"token": None, "expires": None}

# ─── توابع کمکی ──────────────────────────────────────────────────────────────

def is_allowed(user_id: int) -> bool:
    if not ALLOWED_USERS or ALLOWED_USERS == ['']:
        return True
    return str(user_id) in ALLOWED_USERS

def format_bytes(b: int) -> str:
    if not b or b == 0:
        return "0 B"
    if b < 1024:
        return f"{b} B"
    if b < 1024**2:
        return f"{b/1024:.1f} KB"
    if b < 1024**3:
        return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", os.environ.get("HOST", "localhost"))

async def panel_login() -> bool:
    global panel_session
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{PANEL_URL}/api/login",
                json={"password": ADMIN_PASSWORD}
            )
            if resp.status_code == 200:
                cookies = resp.cookies
                if "eagle_session" in cookies:
                    panel_session["token"] = cookies["eagle_session"]
                    panel_session["expires"] = datetime.now() + timedelta(hours=24)
                    return True
            return False
    except Exception as e:
        logger.error(f"Login error: {e}")
        return False

async def panel_request(method: str, endpoint: str, data: dict = None) -> Dict:
    global panel_session
    
    if not panel_session["token"] or panel_session["expires"] < datetime.now():
        if not await panel_login():
            return {"error": "auth_failed"}
    
    url = f"{PANEL_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    cookies = {"eagle_session": panel_session["token"]}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method.upper() == "GET":
                resp = await client.get(url, headers=headers, cookies=cookies)
            elif method.upper() == "POST":
                resp = await client.post(url, json=data, headers=headers, cookies=cookies)
            elif method.upper() == "PATCH":
                resp = await client.patch(url, json=data, headers=headers, cookies=cookies)
            elif method.upper() == "DELETE":
                resp = await client.delete(url, json=data, headers=headers, cookies=cookies)
            else:
                return {"error": "method not supported"}
            
            if resp.status_code == 401:
                if await panel_login():
                    return await panel_request(method, endpoint, data)
                return {"error": "unauthorized"}
            
            try:
                return resp.json()
            except:
                return {"error": f"status: {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ─── کیبوردها ─────────────────────────────────────────────────────────────────

def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📊 داشبورد", callback_data="dashboard")],
        [InlineKeyboardButton("👥 کاربران", callback_data="users")],
        [InlineKeyboardButton("➕ ساخت کاربر", callback_data="create_user")],
        [InlineKeyboardButton("🔌 اتصالات زنده", callback_data="connections")],
        [InlineKeyboardButton("📈 آمار", callback_data="stats")],
        [InlineKeyboardButton("🔄 بکاپ", callback_data="backup")],
        [InlineKeyboardButton("⚙️ تنظیمات پنل", callback_data="settings_panel")],
        [InlineKeyboardButton("❓ راهنما", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_user_actions_keyboard(uuid: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📋 اطلاعات", callback_data=f"user_info_{uuid}")],
        [InlineKeyboardButton("🔗 لینک کانفیگ", callback_data=f"user_link_{uuid}")],
        [InlineKeyboardButton("📎 ساب‌لینک", callback_data=f"user_sub_{uuid}")],
        [InlineKeyboardButton("📊 مصرف", callback_data=f"user_usage_{uuid}")],
        [InlineKeyboardButton("✏️ ویرایش", callback_data=f"user_edit_start_{uuid}")],
        [InlineKeyboardButton("🗑️ حذف", callback_data=f"user_delete_{uuid}")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="users")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_users_keyboard(links: list, page: int = 0) -> InlineKeyboardMarkup:
    per_page = 8
    total = len(links)
    total_pages = (total + per_page - 1) // per_page
    start = page * per_page
    end = min(start + per_page, total)
    
    keyboard = []
    for link in links[start:end]:
        label = link.get('label', 'نامشخص')[:20]
        status = "🟢" if link.get('active') and not link.get('expired') else "🔴"
        keyboard.append([InlineKeyboardButton(f"{status} {label}", callback_data=f"user_{link['uuid']}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"users_page_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"{page+1}/{total_pages}", callback_data="users_page_info"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"users_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("➕ ساخت کاربر جدید", callback_data="create_user")])
    keyboard.append([InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔑 تغییر رمز پنل", callback_data="change_password")],
        [InlineKeyboardButton("🔗 دریافت لینک پنل", callback_data="get_panel_link")],
        [InlineKeyboardButton("📊 وضعیت پنل", callback_data="panel_status")],
        [InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ─── هندلرهای اصلی ──────────────────────────────────────────────────────────

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("❌ شما دسترسی به این ربات ندارید.")
        return
    
    await panel_login()
    
    await update.message.reply_text(
        f"🦅 <b>به پنل عقاب خوش آمدید!</b>\n\n"
        f"📌 <b>کاربر:</b> {update.effective_user.first_name}\n"
        f"🔗 <b>پنل:</b> {PANEL_URL}\n\n"
        f"از دکمه‌های زیر پنل را مدیریت کنید.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

# ─── نمایش کاربران ──────────────────────────────────────────────────────────

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0, query=None):
    resp = await panel_request("GET", "/api/links")
    
    if "error" in resp:
        msg = f"❌ خطا: {resp.get('error')}"
        if query:
            await query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return
    
    links = resp.get("links", [])
    
    if not links:
        msg = "📭 هیچ کاربری ساخته نشده است."
        if query:
            await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ ساخت کاربر جدید", callback_data="create_user")],
                [InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")]
            ]))
        else:
            await update.message.reply_text(msg, reply_markup=get_users_keyboard([]))
        return
    
    total = len(links)
    active = sum(1 for l in links if l.get('active') and not l.get('expired'))
    total_used = sum(l.get('used_bytes', 0) for l in links)
    
    msg = (
        f"👥 <b>لیست کاربران</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📊 <b>کل کاربران:</b> {total}\n"
        f"🟢 <b>فعال:</b> {active}\n"
        f"🔴 <b>غیرفعال:</b> {total - active}\n"
        f"📥 <b>مصرف کل:</b> {format_bytes(total_used)}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"<i>برای مشاهده جزئیات روی کاربر کلیک کنید</i>"
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_users_keyboard(links, page))
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_users_keyboard(links, page))

# ─── نمایش جزئیات کاربر ─────────────────────────────────────────────────────

async def show_user_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, uuid: str, query=None):
    resp = await panel_request("GET", "/api/links")
    
    if "error" in resp:
        if query:
            await query.edit_message_text(f"❌ خطا: {resp.get('error')}")
        return
    
    links = resp.get("links", [])
    link = next((l for l in links if l['uuid'] == uuid), None)
    
    if not link:
        if query:
            await query.edit_message_text("❌ کاربر یافت نشد!")
        return
    
    host = get_host()
    used = link.get('used_bytes', 0)
    limit = link.get('limit_bytes', 0)
    pct = 0 if limit == 0 else min(100, (used / limit) * 100)
    
    # دریافت تعداد اتصالات از API
    conn_resp = await panel_request("GET", "/api/connections")
    conn_count = 0
    if "error" not in conn_resp:
        conns = conn_resp.get("connections", [])
        conn_count = sum(1 for c in conns if c.get("label") == link.get('label'))
    
    msg = (
        f"🦅 <b>اطلاعات کاربر</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📌 <b>نام:</b> {link.get('label', 'نامشخص')}\n"
        f"🔑 <b>UUID:</b> <code>{uuid}</code>\n"
        f"📊 <b>مصرف:</b> {format_bytes(used)}\n"
        f"📦 <b>سهمیه:</b> {format_bytes(limit) if limit > 0 else '∞'}\n"
        f"📈 <b>درصد مصرف:</b> {pct:.1f}%\n"
        f"📱 <b>دستگاه‌ها:</b> {link.get('max_devices', 0) if link.get('max_devices', 0) > 0 else '∞'}\n"
        f"🔄 <b>پروتکل:</b> {link.get('protocol', 'vless-ws')}\n"
        f"🔌 <b>پورت:</b> {link.get('port', 443)}\n"
        f"🔌 <b>اتصالات فعال:</b> {conn_count}\n"
        f"📅 <b>ساخت:</b> {link.get('created_at', 'نامشخص')[:10]}\n"
        f"⏳ <b>انقضا:</b> {link.get('expires_at', 'نامحدود')[:10] if link.get('expires_at') else 'نامحدود'}\n"
        f"🔒 <b>رمزدار:</b> {'✅' if link.get('has_password') else '❌'}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📎 <b>ساب‌لینک:</b>\n"
        f"<code>https://{host}/sub/{uuid}</code>"
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_user_actions_keyboard(uuid))
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_user_actions_keyboard(uuid))

# ─── نمایش آمار ─────────────────────────────────────────────────────────────

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    resp = await panel_request("GET", "/stats")
    
    if "error" in resp:
        msg = f"❌ خطا: {resp.get('error')}"
        if query:
            await query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return
    
    data = resp
    
    msg = (
        f"📈 <b>آمار پنل عقاب</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🔌 <b>اتصالات زنده:</b> {data.get('active_connections', 0)}\n"
        f"👥 <b>کل کاربران:</b> {data.get('links_count', 0)}\n"
        f"🟢 <b>کاربران فعال:</b> {data.get('active_links', 0)}\n"
        f"📥 <b>ترافیک کل:</b> {data.get('total_traffic_mb', 0):.2f} MB\n"
        f"📊 <b>تعداد درخواست‌ها:</b> {data.get('total_requests', 0)}\n"
        f"⏱️ <b>آپ‌تایم:</b> {data.get('uptime', '00:00:00')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>پر مصرف‌ترین:</b> {data.get('top_user', {}).get('label', '—')}\n"
        f"📊 مصرف: {data.get('top_user', {}).get('used_fmt', '0')}"
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())

# ─── نمایش اتصالات زنده ─────────────────────────────────────────────────────

async def show_connections(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    resp = await panel_request("GET", "/api/connections")
    
    if "error" in resp:
        msg = f"❌ خطا: {resp.get('error')}"
        if query:
            await query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return
    
    conns = resp.get("connections", [])
    count = resp.get("count", 0)
    
    if not conns:
        msg = "🔌 هیچ اتصال فعالی وجود ندارد."
        if query:
            await query.edit_message_text(msg, reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(msg, reply_markup=get_main_keyboard())
        return
    
    msg = f"🔌 <b>اتصالات زنده</b> ({count})\n━━━━━━━━━━━━━━━━\n"
    
    for c in conns[:15]:
        ip = c.get('ip', 'نامشخص')
        label = c.get('label', 'نامشخص')
        bytes_fmt = c.get('bytes_fmt', '0 B')
        sessions = c.get('sessions', 0)
        msg += f"🌐 {ip}\n📌 {label}\n📥 {bytes_fmt} | {sessions} اتصال\n━━━━━━━━━━━━━━━━\n"
    
    if len(conns) > 15:
        msg += f"\n<i>و {len(conns)-15} اتصال دیگر...</i>"
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())

# ─── بکاپ ──────────────────────────────────────────────────────────────────

async def show_backup(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    resp = await panel_request("GET", "/api/backup")
    
    if "error" in resp:
        msg = f"❌ خطا: {resp.get('error')}"
        if query:
            await query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return
    
    backup_data = json.dumps(resp, indent=2, ensure_ascii=False)
    filename = f"eagle_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(backup_data)
    
    msg = f"🔄 <b>بکاپ گرفته شد!</b>\n\n📅 زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open(filename, 'rb'),
            filename=filename,
            caption="🦅 فایل بکاپ پنل عقاب"
        )
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open(filename, 'rb'),
            filename=filename,
            caption="🦅 فایل بکاپ پنل عقاب"
        )
    
    os.remove(filename)

# ─── ساخت کاربر ──────────────────────────────────────────────────────────────

async def start_create_user(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    user_id = update.effective_user.id
    pending_actions[user_id] = {
        "action": "create_user",
        "step": "label",
        "data": {}
    }
    
    msg = (
        "➕ <b>ساخت کاربر جدید</b>\n"
        "━━━━━━━━━━━━━━━━\n"
        "📌 لطفاً <b>نام کاربری</b> را وارد کنید:\n"
        "(مثلاً: کاربر علی)\n\n"
        "❌ برای لغو، /cancel را بزنید."
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def process_create_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in pending_actions:
        await update.message.reply_text("❌ عملیات فعالی وجود ندارد.")
        return
    
    action = pending_actions[user_id]
    step = action["step"]
    data = action["data"]
    
    if step == "label":
        data["label"] = text
        pending_actions[user_id]["step"] = "quota"
        await update.message.reply_text(
            "📊 <b>میزان حجم را وارد کنید (GB):</b>\n"
            "(مثلاً: 5 برای 5 گیگابایت)\n\n"
            "💡 عدد 0 به معنای نامحدود است.",
            parse_mode=ParseMode.HTML
        )
    
    elif step == "quota":
        try:
            quota = float(text)
            if quota < 0:
                raise ValueError
            data["quota"] = quota
            pending_actions[user_id]["step"] = "expiry"
            await update.message.reply_text(
                "📅 <b>مدت اعتبار (روز) را وارد کنید:</b>\n"
                "(مثلاً: 30 برای 30 روز)\n\n"
                "💡 عدد 0 به معنای نامحدود است.",
                parse_mode=ParseMode.HTML
            )
        except:
            await update.message.reply_text("❌ عدد معتبر وارد کنید! (مثلاً: 5)")
    
    elif step == "expiry":
        try:
            days = int(text)
            if days < 0:
                raise ValueError
            data["days"] = days
            pending_actions[user_id]["step"] = "devices"
            await update.message.reply_text(
                "📱 <b>محدودیت دستگاه را وارد کنید:</b>\n"
                "(مثلاً: 1 برای یک دستگاه)\n\n"
                "💡 عدد 0 به معنای نامحدود است.",
                parse_mode=ParseMode.HTML
            )
        except:
            await update.message.reply_text("❌ عدد معتبر وارد کنید! (مثلاً: 30)")
    
    elif step == "devices":
        try:
            devices = int(text)
            if devices < 0:
                raise ValueError
            data["devices"] = devices
            pending_actions[user_id]["step"] = "password"
            await update.message.reply_text(
                "🔑 <b>رمز کانفیگ (اختیاری):</b>\n"
                "برای تنظیم رمز، آن را وارد کنید.\n"
                "برای رد کردن، 'ندارد' را بزنید.",
                parse_mode=ParseMode.HTML
            )
        except:
            await update.message.reply_text("❌ عدد معتبر وارد کنید! (مثلاً: 1)")
    
    elif step == "password":
        if text.lower() == "ندارد":
            data["password"] = ""
        else:
            data["password"] = text
        
        await update.message.reply_text("⏳ در حال ساخت کاربر...")
        
        create_data = {
            "label": data["label"],
            "limit_value": data["quota"],
            "limit_unit": "GB",
            "expires_days": data["days"],
            "max_devices": data["devices"],
            "password": data["password"],
            "fingerprint": "chrome",
            "protocol": "vless-ws",
            "port": 443
        }
        
        resp = await panel_request("POST", "/api/links", create_data)
        
        if "error" in resp:
            await update.message.reply_text(f"❌ خطا در ساخت کاربر: {resp.get('error')}")
        else:
            host = get_host()
            msg = (
                f"✅ <b>کاربر با موفقیت ساخته شد!</b>\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📌 <b>نام:</b> {data['label']}\n"
                f"🔑 <b>UUID:</b> <code>{resp.get('uuid', '')}</code>\n"
                f"📊 <b>حجم:</b> {data['quota']} GB\n"
                f"📱 <b>دستگاه:</b> {data['devices'] if data['devices'] > 0 else '∞'}\n"
                f"📅 <b>اعتبار:</b> {data['days'] if data['days'] > 0 else '∞'} روز\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"🔗 <b>لینک کانفیگ:</b>\n"
                f"<code>{resp.get('vless_link', '')}</code>\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📎 <b>ساب‌لینک:</b>\n"
                f"<code>https://{host}/sub/{resp.get('uuid', '')}</code>"
            )
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())
        
        del pending_actions[user_id]

# ─── ویرایش کاربر ──────────────────────────────────────────────────────────

async def start_edit_user(update: Update, context: ContextTypes.DEFAULT_TYPE, uuid: str, query=None):
    user_id = update.effective_user.id
    
    resp = await panel_request("GET", "/api/links")
    link = next((l for l in resp.get("links", []) if l['uuid'] == uuid), None)
    
    if not link:
        if query:
            await query.edit_message_text("❌ کاربر یافت نشد!")
        return
    
    pending_actions[user_id] = {
        "action": "edit_user",
        "step": "label",
        "data": {"uuid": uuid, "old_label": link.get('label', '')}
    }
    
    msg = (
        f"✏️ <b>ویرایش کاربر</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📌 <b>نام فعلی:</b> {link.get('label', 'نامشخص')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"نام جدید را وارد کنید (یا 'بی‌تغییر' برای حفظ):"
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def process_edit_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in pending_actions or pending_actions[user_id]["action"] != "edit_user":
        await update.message.reply_text("❌ عملیات ویرایش فعالی وجود ندارد.")
        return
    
    action = pending_actions[user_id]
    data = action["data"]
    uuid = data["uuid"]
    
    update_data = {}
    
    if text.lower() != "بی‌تغییر":
        update_data["label"] = text
    else:
        update_data["label"] = data["old_label"]
    
    resp = await panel_request("GET", "/api/links")
    link = next((l for l in resp.get("links", []) if l['uuid'] == uuid), None)
    
    if link and link.get('has_password'):
        await update.message.reply_text("🔑 این کانفیگ رمزدار است. رمز آن را وارد کنید:")
        pending_actions[user_id]["step"] = "password"
        pending_actions[user_id]["update_data"] = update_data
        return
    
    result = await panel_request("PATCH", f"/api/links/{uuid}", {**update_data, "password": ""})
    
    if "error" in result:
        await update.message.reply_text(f"❌ خطا: {result.get('error')}")
    else:
        await update.message.reply_text("✅ کاربر با موفقیت ویرایش شد!", reply_markup=get_main_keyboard())
    
    del pending_actions[user_id]

async def process_edit_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    password = update.message.text.strip()
    
    if user_id not in pending_actions:
        return
    
    action = pending_actions[user_id]
    uuid = action["data"]["uuid"]
    update_data = action.get("update_data", {})
    
    result = await panel_request("PATCH", f"/api/links/{uuid}", {**update_data, "password": password})
    
    if "error" in result:
        if result.get('error') == 'رمز کانفیگ اشتباه است':
            await update.message.reply_text("❌ رمز کانفیگ اشتباه است! دوباره تلاش کنید:")
            return
        await update.message.reply_text(f"❌ خطا: {result.get('error')}")
    else:
        await update.message.reply_text("✅ کاربر با موفقیت ویرایش شد!", reply_markup=get_main_keyboard())
    
    del pending_actions[user_id]

# ─── حذف کاربر ──────────────────────────────────────────────────────────────

async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE, uuid: str, query=None):
    resp = await panel_request("GET", "/api/links")
    link = next((l for l in resp.get("links", []) if l['uuid'] == uuid), None)
    label = link.get('label', 'نامشخص') if link else 'نامشخص'
    
    if link and link.get('has_password'):
        user_id = update.effective_user.id
        pending_actions[user_id] = {
            "action": "delete_user_with_password",
            "uuid": uuid,
            "label": label
        }
        
        msg = f"🔑 کاربر «{label}» رمزدار است. برای حذف، رمز آن را وارد کنید:"
        if query:
            await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ بله، حذف کن", callback_data=f"confirm_delete_{uuid}")],
        [InlineKeyboardButton("❌ لغو", callback_data=f"user_{uuid}")],
    ]
    msg = f"⚠️ <b>آیا از حذف کاربر «{label}» مطمئن هستید؟</b>"
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

async def confirm_delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE, uuid: str, query=None):
    resp = await panel_request("DELETE", f"/api/links/{uuid}", {"password": ""})
    
    if "error" in resp:
        msg = f"❌ خطا: {resp.get('error')}"
    else:
        msg = "✅ کاربر با موفقیت حذف شد!"
    
    if query:
        await query.edit_message_text(msg, reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(msg, reply_markup=get_main_keyboard())

# ─── تغییر رمز پنل ──────────────────────────────────────────────────────────

async def start_change_password(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    user_id = update.effective_user.id
    pending_actions[user_id] = {
        "action": "change_password",
        "step": "old_password"
    }
    
    msg = (
        "🔑 <b>تغییر رمز پنل</b>\n"
        "━━━━━━━━━━━━━━━━\n"
        "🔐 <b>رمز فعلی</b> را وارد کنید:\n\n"
        "💡 رمز پیش‌فرض: 123456"
    )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

async def process_change_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if user_id not in pending_actions or pending_actions[user_id]["action"] != "change_password":
        await update.message.reply_text("❌ عملیات فعالی وجود ندارد.")
        return
    
    action = pending_actions[user_id]
    step = action["step"]
    
    if step == "old_password":
        action["old_password"] = text
        action["step"] = "new_password"
        await update.message.reply_text(
            "🔑 <b>رمز جدید</b> را وارد کنید:\n\n"
            "💡 حداقل ۴ کاراکتر",
            parse_mode=ParseMode.HTML
        )
    
    elif step == "new_password":
        if len(text) < 4:
            await update.message.reply_text("❌ رمز باید حداقل ۴ کاراکتر باشد! دوباره وارد کنید:")
            return
        
        action["new_password"] = text
        action["step"] = "confirm_password"
        await update.message.reply_text(
            "✅ <b>تکرار رمز جدید:</b>",
            parse_mode=ParseMode.HTML
        )
    
    elif step == "confirm_password":
        if text != action["new_password"]:
            await update.message.reply_text("❌ رمزها مطابقت ندارند! دوباره تلاش کنید:")
            return
        
        result = await panel_request("POST", "/api/settings/password", {
            "old_password": action["old_password"],
            "new_password": action["new_password"]
        })
        
        if "error" in result:
            await update.message.reply_text(f"❌ خطا: {result.get('error')}")
        else:
            await update.message.reply_text(
                f"✅ <b>رمز پنل با موفقیت تغییر کرد!</b>\n\n"
                f"🔑 رمز جدید: <code>{action['new_password']}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=get_main_keyboard()
            )
            global ADMIN_PASSWORD
            ADMIN_PASSWORD = action["new_password"]
            panel_session["token"] = None
        
        del pending_actions[user_id]

# ─── دریافت لینک پنل ────────────────────────────────────────────────────────

async def get_panel_link(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    host = get_host()
    panel_url = f"https://{host}"
    msg = (
        f"🔗 <b>لینک پنل عقاب</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🌐 <b>آدرس پنل:</b>\n"
        f"<code>{panel_url}</code>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🔑 <b>رمز ورود:</b> <code>{ADMIN_PASSWORD}</code>"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 کپی لینک", callback_data=f"copy_{panel_url}")],
        [InlineKeyboardButton("🔙 منوی تنظیمات", callback_data="settings_panel")],
    ]
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

# ─── وضعیت پنل ──────────────────────────────────────────────────────────────

async def panel_status(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    resp = await panel_request("GET", "/stats")
    
    if "error" in resp:
        msg = f"❌ <b>وضعیت پنل: قطع</b>\n\nخطا: {resp.get('error')}"
    else:
        data = resp
        msg = (
            f"✅ <b>وضعیت پنل: متصل</b>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"🔗 <b>آدرس:</b> {PANEL_URL}\n"
            f"👥 <b>کاربران:</b> {data.get('links_count', 0)}\n"
            f"🟢 <b>فعال:</b> {data.get('active_links', 0)}\n"
            f"🔌 <b>اتصالات:</b> {data.get('active_connections', 0)}\n"
            f"📥 <b>ترافیک:</b> {data.get('total_traffic_mb', 0):.2f} MB\n"
            f"⏱️ <b>آپ‌تایم:</b> {data.get('uptime', '00:00:00')}"
        )
    
    if query:
        await query.edit_message_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_settings_keyboard())
    else:
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML, reply_markup=get_settings_keyboard())

# ─── کال‌بک هندلر ────────────────────────────────────────────────────────────

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await query.edit_message_text("❌ دسترسی غیرمجاز!")
        return
    
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text(
            "🦅 <b>منوی اصلی پنل عقاب</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    elif data == "users":
        await show_users(update, context, page=0, query=query)
    
    elif data.startswith("users_page_"):
        page = int(data.split("_")[-1]) if data.split("_")[-1].isdigit() else 0
        await show_users(update, context, page=page, query=query)
    
    elif data.startswith("user_"):
        uuid = data.replace("user_", "")
        await show_user_detail(update, context, uuid, query=query)
    
    elif data.startswith("user_info_"):
        uuid = data.replace("user_info_", "")
        await show_user_detail(update, context, uuid, query=query)
    
    elif data.startswith("user_link_"):
        uuid = data.replace("user_link_", "")
        resp = await panel_request("GET", "/api/links")
        link = next((l for l in resp.get("links", []) if l['uuid'] == uuid), None)
        if link and link.get('vless_link'):
            await query.edit_message_text(
                f"🔗 <b>لینک کانفیگ</b>\n\n<code>{link.get('vless_link')}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📋 کپی", callback_data=f"copy_{link.get('vless_link')}")],
                    [InlineKeyboardButton("🔙 برگشت", callback_data=f"user_{uuid}")]
                ])
            )
    
    elif data.startswith("user_sub_"):
        uuid = data.replace("user_sub_", "")
        host = get_host()
        sub_link = f"https://{host}/sub/{uuid}"
        await query.edit_message_text(
            f"📎 <b>ساب‌لینک</b>\n\n<code>{sub_link}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 کپی", callback_data=f"copy_{sub_link}")],
                [InlineKeyboardButton("🔙 برگشت", callback_data=f"user_{uuid}")]
            ])
        )
    
    elif data.startswith("user_usage_"):
        uuid = data.replace("user_usage_", "")
        resp = await panel_request("GET", "/api/links")
        link = next((l for l in resp.get("links", []) if l['uuid'] == uuid), None)
        if link:
            used = link.get('used_bytes', 0)
            limit = link.get('limit_bytes', 0)
            pct = 0 if limit == 0 else min(100, (used / limit) * 100)
            today_bytes = link.get('today_bytes', 0)
            
            msg = (
                f"📊 <b>مصرف کاربر</b>\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📌 <b>نام:</b> {link.get('label', 'نامشخص')}\n"
                f"📥 <b>مصرف کل:</b> {format_bytes(used)}\n"
                f"📊 <b>مصرف امروز:</b> {format_bytes(today_bytes)}\n"
                f"📦 <b>سهمیه:</b> {format_bytes(limit) if limit > 0 else '∞'}\n"
                f"📈 <b>درصد:</b> {pct:.1f}%"
            )
            await query.edit_message_text(
                msg,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 برگشت", callback_data=f"user_{uuid}")]
                ])
            )
    
    elif data.startswith("user_edit_start_"):
        uuid = data.replace("user_edit_start_", "")
        await start_edit_user(update, context, uuid, query=query)
    
    elif data.startswith("user_delete_"):
        uuid = data.replace("user_delete_", "")
        await delete_user(update, context, uuid, query=query)
    
    elif data.startswith("confirm_delete_"):
        uuid = data.replace("confirm_delete_", "")
        await confirm_delete_user(update, context, uuid, query=query)
    
    elif data == "create_user":
        await start_create_user(update, context, query=query)
    
    elif data == "stats":
        await show_stats(update, context, query=query)
    
    elif data == "connections":
        await show_connections(update, context, query=query)
    
    elif data == "backup":
        await show_backup(update, context, query=query)
    
    elif data == "dashboard":
        await show_stats(update, context, query=query)
    
    elif data == "settings_panel":
        await query.edit_message_text(
            "⚙️ <b>تنظیمات پنل عقاب</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_settings_keyboard()
        )
    
    elif data == "change_password":
        await start_change_password(update, context, query=query)
    
    elif data == "get_panel_link":
        await get_panel_link(update, context, query=query)
    
    elif data == "panel_status":
        await panel_status(update, context, query=query)
    
    elif data.startswith("copy_"):
        text_to_copy = data.replace("copy_", "")
        await query.edit_message_text(
            f"📋 <b>متن کپی شد!</b>\n\n<code>{text_to_copy}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
            ])
        )
    
    elif data == "help":
        await query.edit_message_text(
            "🦅 <b>راهنمای ربات پنل عقاب</b>\n\n"
            "📌 <b>قابلیت‌ها:</b>\n"
            "• 📊 داشبورد - آمار کلی\n"
            "• 👥 کاربران - لیست و مدیریت\n"
            "• ➕ ساخت کاربر - ساخت کاربر جدید\n"
            "• 🔌 اتصالات زنده - اتصالات فعال\n"
            "• 📈 آمار - آمار کامل\n"
            "• 🔄 بکاپ - گرفتن بکاپ\n"
            "• ⚙️ تنظیمات - تغییر رمز و لینک",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )

# ─── هندلر پیام ──────────────────────────────────────────────────────────────

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_allowed(user_id):
        await update.message.reply_text("❌ دسترسی غیرمجاز!")
        return
    
    text = update.message.text
    
    if text.startswith("/cancel"):
        if user_id in pending_actions:
            action = pending_actions[user_id]
            action_name = action.get("action", "")
            del pending_actions[user_id]
            await update.message.reply_text(f"✅ عملیات '{action_name}' لغو شد.", reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text("❌ عملیات فعالی وجود ندارد.")
        return
    
    if user_id in pending_actions:
        action = pending_actions[user_id]
        
        if action["action"] == "create_user":
            await process_create_user(update, context)
            return
        
        elif action["action"] == "edit_user":
            if action.get("step") == "password":
                await process_edit_password(update, context)
            else:
                await process_edit_user(update, context)
            return
        
        elif action["action"] == "change_password":
            await process_change_password(update, context)
            return
        
        elif action["action"] == "delete_user_with_password":
            uuid = action["uuid"]
            password = text
            result = await panel_request("DELETE", f"/api/links/{uuid}", {"password": password})
            
            if "error" in result:
                if result.get('error') == 'رمز کانفیگ اشتباه است':
                    await update.message.reply_text("❌ رمز کانفیگ اشتباه است! دوباره تلاش کنید:")
                    return
                await update.message.reply_text(f"❌ خطا: {result.get('error')}")
            else:
                await update.message.reply_text(f"✅ کاربر «{action.get('label', '')}» حذف شد!", reply_markup=get_main_keyboard())
            
            del pending_actions[user_id]
            return
    
    await update.message.reply_text(
        "❌ دستور ناشناخته!\nاز /menu استفاده کنید.",
        reply_markup=get_main_keyboard()
    )

# ─── اجرای ربات ──────────────────────────────────────────────────────────────

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", start_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    logger.info("🦅 ربات پنل عقاب شروع به کار کرد!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
