from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests
import json

# توکن ربات تلگرام
TOKEN = ""

# کلید API جمینی
GEMINI_API_KEY = ""
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# تابع برای گرفتن پاسخ از جمینی
def get_gemini_response(question):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"مشکلی پیش اومد: {response.status_code} - {response.text}"

# تابع خوش‌آمدگویی برای دستور /start
async def start(update: Update, context):
    welcome_message = "*هر چیزی که می‌خوای از من بپرس، من جواب می‌دم!*"
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# تابع مدیریت پیام‌ها
async def handle_message(update: Update, context):
    user_message = update.message.text  # پیام کاربر
    gemini_reply = get_gemini_response(user_message)  # گرفتن پاسخ از جمینی
    # فرمت Markdown برای پاسخ
    formatted_reply = f"*{user_message}*\n\n{gemini_reply}"
    await update.message.reply_text(formatted_reply, parse_mode="Markdown")

# راه‌اندازی ربات
def main():
    # ساخت اپلیکیشن
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))  # هندلر برای /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # هندلر برای پیام‌های متنی

    # شروع ربات
    application.run_polling()

if __name__ == "__main__":
    main()