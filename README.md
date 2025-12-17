# Telegram-бот аналитики видео

Бот принимает вопросы на русском языке и возвращает одно число.

## Запуск

1. Создайте `.env` на основе `.env.example`
2. Запустите БД и загрузите данные:
   ```bash
   docker-compose up -d db
   python scripts/load_data.py data/videos.json