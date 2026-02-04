import telebot
from telebot import types
import requests
from io import BytesIO

# ========= CONFIG =========
BOT_TOKEN = "8483155468:AAEUBHJxlJRPsDyd3jFIJmErsPbDPDv-q6c"
REMOVE_BG_API_KEY = "y4VxAJvmTnSvud2p3UxvxxvQ"

CHANNEL_USERNAME = "@mixxrt"
CHANNEL_LINK = "https://t.me/mixxrt"

UPI_ID = "9861172719@fam"
PREMIUM_PRICE = "₹10"
# ==========================

bot = telebot.TeleBot(BOT_TOKEN)
user_photos = {}

# ---------- FORCE JOIN ----------
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def force_join(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Join Channel", url= https://t.me/mixxrt)
    bot.send_message(
        chat_id,
        "❌ You must join our channel to use this bot.\n\nAfter joining, press /start again.",
        reply_markup=markup
    )

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(message):
    uid = message.from_user.id
    name = message.from_user.first_name

    if not is_joined(uid):
        force_join(message.chat.id)
        return

    caption = (
        f"👋 Welcome {name}\n"
        f"🆔 User ID: {uid}\n\n"
        "📸 Send your photo to remove background.\n"
        "HD is FREE • 4K ULTRA is Premium"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 My Channel", url= https://t.me/mixxrt)

    bot.send_photo(
        message.chat.id,
        open("start.jpg", "rb"),
        caption=caption,
        reply_markup=markup
    )

# ---------- PHOTO ----------
@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    if not is_joined(message.from_user.id):
        force_join(message.chat.id)
        return

    user_photos[message.from_user.id] = message.photo[-1].file_id

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("✅ HD (FREE)", callback_data="hd"),
        types.InlineKeyboardButton("💎 4K ULTRA (₹10)", callback_data="4k"),
        types.InlineKeyboardButton("📢 My Channel", url=https://t.me/mixxrt)
    )

    bot.send_message(
        message.chat.id,
        "Choose quality:",
        reply_markup=markup
    )

# ---------- REMOVE BG ----------
def remove_bg(image_bytes):
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": image_bytes},
        data={"size": "auto"},
        headers={"X-Api-Key": y4VxAJvmTnSvud2p3UxvxxvQ
    )
    if r.status_code == 200:
        return r.content
    return None

# ---------- CALLBACK ----------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = call.from_user.id

    if uid not in user_photos:
        bot.answer_callback_query(call.id, "Send photo first.")
        return

    if call.data == "hd":
        file_info = bot.get_file(user_photos[uid])
        image = bot.download_file(file_info.file_path)

        bot.edit_message_text(
            "⏳ Processing HD image...",
            call.message.chat.id,
            call.message.message_id
        )

        result = remove_bg(BytesIO(image))

        if result:
            out = BytesIO(result)
            out.name = "bg_removed_hd.png"
            bot.send_document(
                call.message.chat.id,
                out,
                caption="✅ HD Background Removed (PNG)"
            )
        else:
            bot.send_message(call.message.chat.id, "❌ Failed. Try again.")

    elif call.data == "4k":
        bot.send_message(
            call.message.chat.id,
            f"💎 4K ULTRA PREMIUM\n\n"
            f"Price: {PREMIUM_PRICE}\n"
            f"UPI ID:\n{UPI_ID}\n\n"
            "After payment, send screenshot to admin.\n"
            "4K ULTRA gives best quality PNG."
        )

# ---------- RUN ----------
print("🤖 Bot is running...")
bot.polling(non_stop=True)
