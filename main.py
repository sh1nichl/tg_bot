import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = FastAPI()
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Установим webhook при запуске FastAPI
@app.on_event("startup")
async def startup():
    await telegram_app.bot.set_webhook("https://tg-bot-1-b1up.onrender.com/webhook")
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Обработка webhook-запросов от Telegram
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# Ответ на /start (необязательный, просто для теста)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("отправь любое сообщение!")

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_msg = message.text

    # Отправка админу
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🌊 у тебя новое анонимное сообщение:\n\n{user_msg}\n\n↩️ свайпни влево для ответа."
    )

    # Ответ пользователю
    reply = await message.reply_text("сообщение отправлено анонимно. ожидайте ответа.")

    # Удаление сообщений через 10 секунд
    await asyncio.sleep(10)
    try:
        await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        await context.bot.delete_message(chat_id=reply.chat_id, message_id=reply.message_id)
    except:
        pass
