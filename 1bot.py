import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# Укажи свой токен и ID
BOT_TOKEN = os.environ.get("8015495045:AAEHRbMDYJ0lM-fOttvXVanZAac8PEP8RHo")
ADMIN_ID = int(os.environ.get("1114004611"))  # пример: 123456789

app = FastAPI()
telegram_app = Application.builder().token("8015495045:AAEHRbMDYJ0lM-fOttvXVanZAac8PEP8RHo").build()

# Обработка анонимных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    await context.bot.send_message(
        chat_id=1114004611,
        text=f"🌊 у тебя новое анонимное сообщение:\n\n{text}\n\n↩️ свайпни влево для ответа."
    )
    await message.reply_text("сообщение отправлено анонимно. ожидайте ответа.")
    await asyncio.sleep(10)
    try:
        await message.delete()
    except Exception:
        pass  # Игнорируем ошибку, если сообщение удалить не удалось

# Настройка webhook
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# Запуск при старте
@app.on_event("startup")
async def startup():
    await telegram_app.bot.set_webhook("https://telegram_bot.onrender.com/webhook")
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Пустая главная страница
@app.get("/")
async def root():
    return {"message": "бот работает"}
