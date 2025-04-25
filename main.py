import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from fastapi import FastAPI, Request
import asyncio

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = FastAPI()
telegram_app = ApplicationBuilder().token(TOKEN).build()

@app.post("/webhook")
async def webhook(request: Request):
    update = Update.de_json(data=await request.json(), bot=telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # ничего не отправляет при /start

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_msg = message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🌊 у тебя новое анонимное сообщение:\n\n{user_msg}\n\n↩️ свайпни влево для ответа.",
    )
    reply = await message.reply_text("сообщение отправлено анонимно. ожидайте ответа.")
    await asyncio.sleep(10)
    await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
    await context.bot.delete_message(chat_id=reply.chat_id, message_id=reply.message_id)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def set_webhook():
    await telegram_app.bot.set_webhook("https://tg-bot.onrender.com/webhook")

asyncio.run(set_webhook())
