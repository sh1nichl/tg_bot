import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# ЗАМЕНИ эти значения на свои:
ADMIN_ID = 1114004611  # ← сюда вставь свой Telegram ID
BOT_TOKEN = "8015495045:AAEHRbMDYJ0lM-fOttvXVanZAac8PEP8RHo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("приветствую. пиши сюда все, что только душа пожелает. Шини не узнает, что это был/а ты.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    # Отправка сообщения админу
    await context.bot.send_message(
        chat_id=1114004611, 
        text=f"🌊 у тебя новое анонимное сообщение:\n\n{message_text}\n\n↩️ свайпни влево для ответа."
    )
    # Ответ пользователю, что сообщение отправлено анонимно
    await update.message.reply_text("сообщение отправлено анонимно. ожидайте ответа.")
    # Задержка перед удалением сообщения
    await asyncio.sleep(5)  # Ожидание 5 секунды
    # Удаление сообщения пользователя
    await update.message.delete()

# Создание приложения с токеном бота
app = ApplicationBuilder().token("8015495045:AAEHRbMDYJ0lM-fOttvXVanZAac8PEP8RHo").build()

# Добавляем обработчики команд и сообщений
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
app.run_polling()
