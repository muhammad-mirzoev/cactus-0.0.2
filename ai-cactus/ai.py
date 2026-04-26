#           КАКТУС 0.0.2 - ИИ (GPT)
#    Общение с OpenAI для умных ответов

import requests
from config import OPENAI_API_KEY, GPT_MODEL, GPT_MAX_TOKENS, GPT_SYSTEM_PROMPT


def ask_gpt(question: str) -> str:
    """
    Отправляет вопрос в GPT и возвращает текстовый ответ.
    При ошибке возвращает сообщение об ошибке (строку).
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-..."):
        return "ИИ не настроен. Пропиши свой API-ключ OpenAI в файле config.py."

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GPT_MODEL,
        "max_tokens": GPT_MAX_TOKENS,
        "messages": [
            {"role": "system", "content": GPT_SYSTEM_PROMPT},
            {"role": "user",   "content": question},
        ],
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15,
        )
        data = response.json()

        if response.status_code == 200:
            return data["choices"][0]["message"]["content"].strip()

        error_msg = data.get("error", {}).get("message", "неизвестная ошибка")
        return f"Ошибка GPT: {error_msg}"

    except requests.exceptions.ConnectionError:
        return "Нет соединения с интернетом для запроса к ИИ."
    except Exception as e:
        return f"Ошибка при обращении к ИИ: {e}"
