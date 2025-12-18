# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from config.settings import BOT_TOKEN
from bot.handlers import handle_text_message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не установлен в .env")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Обработка любого текстового сообщения
    dp.message.register(handle_text_message)

    # (Опционально) можно добавить /start
    @dp.message(CommandStart())
    async def send_welcome(message):
        await message.answer("Привет! Задавайте вопросы на русском языке об аналитике видео.")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())