# bot/nlp.py
import re
from typing import Optional, Dict, Any
from dateparser import parse
from datetime import datetime, date

def normalize_text(text: str) -> str:
    """Приводим текст к нижнему регистру, убираем лишние пробелы."""
    return re.sub(r'\s+', ' ', text.strip().lower())

def extract_single_date(text: str) -> Optional[date]:
    """Извлекает одну дату из текста (например, '28 ноября 2025')."""
    # Ищем фразы вида "28 ноября 2025", "1 ноября", и т.п.
    date_match = parse(text, languages=['ru'])
    if date_match:
        return date_match.date()
    return None

def extract_date_range(text: str) -> Optional[tuple[date, date]]:
    """Извлекает диапазон дат: 'с 1 по 5 ноября 2025'."""
    # Поддерживаем форматы:
    # - "с 1 по 5 ноября 2025"
    # - "с 1 ноября по 5 ноября 2025"
    # - "с 1 ноября 2025 по 5 ноября 2025"
    pattern = r"с\s+(\d{1,2}(?:\s+\w+)?(?:\s+\d{4})?)\s+по\s+(\d{1,2}(?:\s+\w+)?(?:\s+\d{4})?)"
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None

    start_str, end_str = match.groups()
    # Если в start_str нет года, но он есть в end_str — подставим
    if not re.search(r'\d{4}', start_str) and re.search(r'\d{4}', end_str):
        year = re.search(r'(\d{4})', end_str).group(1)
        start_str += f" {year}"

    start_date = parse(start_str, languages=['ru'])
    end_date = parse(end_str, languages=['ru'])

    if start_date and end_date:
        return start_date.date(), end_date.date()
    return None

def extract_number(text: str) -> Optional[int]:
    """Извлекает число из фразы вида 'больше 100 000 просмотров'."""
    # Убираем пробелы внутри чисел: "100 000" → "100000"
    text_clean = re.sub(r'(\d)\s+(\d)', r'\1\2', text)
    match = re.search(r'(\d+)', text_clean)
    if match:
        return int(match.group(1))
    return None

def parse_query(text: str) -> Optional[Dict[str, Any]]:
    """
    Парсит запрос и возвращает структурированный объект.
    Возвращает None, если запрос не распознан.
    """
    original_text = text
    text = normalize_text(text)

   
    if re.search(r"сколько всего видео", text):
        return {"type": "count_all_videos"}

    # 2. Видео у креатора за период
    creator_match = re.search(r"креатора с id\s*(\d+)", text)
    if creator_match:
        date_range = extract_date_range(text)
        if date_range:
            return {
                "type": "count_videos_by_creator_and_date",
                "creator_id": int(creator_match.group(1)),
                "date_from": date_range[0],
                "date_to": date_range[1]
            }

   
    if "просмотров" in text and ("больше" in text or "набрало" in text):
        threshold = extract_number(text)
        if threshold is not None:
            return {
                "type": "count_videos_with_views_gt",
                "threshold": threshold
            }

    
    if re.search(r"на сколько.*просмотров.*выросли.*\d", text):
        d = extract_single_date(text)
        if d:
            return {
                "type": "sum_delta_views_on_date",
                "date": d
            }

    
    if re.search(r"сколько.*видео.*получали.*новые.*просмотры", text):
        d = extract_single_date(text)
        if d:
            return {
                "type": "count_videos_with_delta_views_on_date",
                "date": d
            }

    
    return None