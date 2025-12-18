from aiogram.types import Message
from bot.nlp import parse_query
from db.queries import (
    count_all_videos,
    count_videos_by_creator_and_date,
    count_videos_with_views_gt,
    sum_delta_views_on_date,
    count_videos_with_delta_views_on_date
)

async def handle_text_message(message: Message) -> None:
    """
    Обрабатывает любое текстовое сообщение от пользователя.
    Отправляет одно число или сообщение об ошибке.
    """
    user_text = message.text.strip()
    parsed = parse_query(user_text)

    if not parsed:
        await message.answer("Не удалось распознать запрос. Попробуйте переформулировать.")
        return

    try:
        query_type = parsed["type"]
        result = None

        if query_type == "count_all_videos":
            result = count_all_videos()

        elif query_type == "count_videos_by_creator_and_date":
            result = count_videos_by_creator_and_date(
                creator_id=parsed["creator_id"],
                date_from=parsed["date_from"],
                date_to=parsed["date_to"]
            )

        elif query_type == "count_videos_with_views_gt":
            result = count_videos_with_views_gt(threshold=parsed["threshold"])

        elif query_type == "sum_delta_views_on_date":
            result = sum_delta_views_on_date(target_date=parsed["date"])

        elif query_type == "count_videos_with_delta_views_on_date":
            result = count_videos_with_delta_views_on_date(target_date=parsed["date"])

        else:
            await message.answer("Неизвестный тип запроса.")
            return

        # Отправляем только число — как того требует ТЗ
        await message.answer(str(result))

    except Exception as e:
        
        await message.answer("Ошибка при обработке запроса.")