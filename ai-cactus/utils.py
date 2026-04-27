#           КАКТУС 0.0.2 - УТИЛИТЫ

import re
import webbrowser
import requests
import urllib.parse
from config import WEATHER_API_KEY, SEARCH_ENGINE


#  ПОГОДА
def get_weather(city: str) -> str:
    """Возвращает строку с погодой для указанного города."""
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "lang": "ru",
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if response.status_code == 200:
            description = data["weather"][0]["description"]
            temp = round(data["main"]["temp"])
            feels_like = round(data["main"]["feels_like"])
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            return (
                f"В городе {city}: {description}. "
                f"Температура {temp}°C, ощущается как {feels_like}°C. "
                f"Влажность {humidity}%, ветер {wind} м/с."
            )

        return f"Не удалось получить погоду: {data.get('message', 'неизвестная ошибка')}."

    except requests.exceptions.ConnectionError:
        return "Нет соединения с интернетом."
    except Exception as e:
        return f"Ошибка при запросе погоды: {e}"


#  БРАУЗЕР
def open_url(url: str) -> None:
    """Открывает ссылку в браузере по умолчанию."""
    webbrowser.open(url)


def web_search(query: str) -> None:
    """Открывает поиск в браузере по запросу."""
    encoded = urllib.parse.quote_plus(query)
    if SEARCH_ENGINE == "yandex":
        url = f"https://yandex.ru/search/?text={encoded}"
    else:
        url = f"https://www.google.com/search?q={encoded}"
    open_url(url)


#  YOUTUBE
def get_first_youtube_video_id(query: str) -> str | None:
    """
    Возвращает ID первого видео YouTube по поисковому запросу.
    Скрейпит страницу результатов (без API-ключа).
    """
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", response.text)
        # Убираем дубликаты, берём первый уникальный
        seen = set()
        for vid_id in ids:
            if vid_id not in seen:
                return vid_id
            seen.add(vid_id)
        return None
    except Exception:
        return None


#  WIKIPEDIA — быстрый ответ
def get_wiki_summary(query: str) -> str:
    """Возвращает краткое описание из Wikipedia на русском."""
    try:
        headers = {
            "User-Agent": "CactusAssistant/0.0.2 (educational project; Python/requests)"
        }
        url = "https://ru.wikipedia.org/w/api.php"

        # Шаг 1 — ищем статью
        search_resp = requests.get(url, headers=headers, timeout=5, params={
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        })
        results = search_resp.json().get("query", {}).get("search", [])

        if not results:
            return ""

        # Шаг 2 — берём первые 3 предложения
        page_title = results[0]["title"]
        summary_resp = requests.get(url, headers=headers, timeout=5, params={
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": page_title,
            "format": "json",
            "exsentences": 3,
        })
        pages = summary_resp.json().get("query", {}).get("pages", {})
        extract = next(iter(pages.values())).get("extract", "").strip()

        return f"{page_title}. {extract}" if extract else ""

    except Exception as e:
        print(f"[!] Ошибка Wikipedia: {e}")
        return ""