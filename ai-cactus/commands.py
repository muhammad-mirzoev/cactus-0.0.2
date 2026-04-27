#             КАКТУС 0.0.2 - КОМАНДЫ
#
# Как работает роутер команд:
#   1. Ищем совпадение ключевых слов в команде.
#   2. Выполняем соответствующую функцию-обработчик.
#   3. Если ничего не нашли — передаём фразу в GPT.
#
# Добавить новую команду:
#   1. Написать функцию-обработчик _cmd_<название>.
#   2. Добавить её в словарь COMMAND_ROUTER внизу файла.

import time
import subprocess
import platform

from speech import speak
from utils import get_weather, open_url, web_search, get_first_youtube_video_id, get_wiki_summary
from ai import ask_gpt

# Определяем ОС один раз при старте
OS = platform.system()  # "Darwin" = macOS, "Windows", "Linux"


#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def _open_app(mac_name: str, win_name: str = None) -> None:
    """Открывает приложение в зависимости от ОС."""
    if OS == "Darwin":
        subprocess.run(["open", "-a", mac_name])
    elif OS == "Windows":
        name = win_name or mac_name
        subprocess.run(["start", name], shell=True)
    else:
        speak("Открытие приложений поддерживается только на macOS и Windows.")


def _extract(command: str, keyword: str) -> str:
    """Вырезает часть строки после ключевого слова."""
    return command.split(keyword, 1)[-1].strip()


#  ОБРАБОТЧИКИ КОМАНД
# Системные

def _cmd_time(command: str) -> None:
    current_time = time.strftime("%H:%M")
    speak(f"Сейчас {current_time}.")


def _cmd_date(command: str) -> None:
    today = time.strftime("%d %B %Y года")
    speak(f"Сегодня {today}.")


def _cmd_hello(command: str) -> None:
    speak("Здесь, слушаю вас!")


def _cmd_welcome_back(command: str) -> None:
    speak("С возвращением! Как съездили?")


def _cmd_shutdown(command: str) -> None:
    speak("Выключаю компьютер. До свидания!")
    if OS == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
    elif OS == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "5"])


def _cmd_restart(command: str) -> None:
    speak("Перезагружаю компьютер.")
    if OS == "Darwin":
        subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])
    elif OS == "Windows":
        subprocess.run(["shutdown", "/r", "/t", "5"])


def _cmd_sleep(command: str) -> None:
    speak("Перевожу компьютер в режим сна.")
    if OS == "Darwin":
        subprocess.run(["pmset", "sleepnow"])
    elif OS == "Windows":
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])


def _cmd_volume_up(command: str) -> None:
    speak("Громче.")
    if OS == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])


def _cmd_volume_down(command: str) -> None:
    speak("Тише.")
    if OS == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])


def _cmd_mute(command: str) -> None:
    speak("Отключаю звук.")
    if OS == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output muted true"])


def _cmd_screenshot(command: str) -> None:
    speak("Делаю скриншот.")
    if OS == "Darwin":
        subprocess.run(["screencapture", "-i", f"~/Desktop/screenshot_{int(time.time())}.png"])
    elif OS == "Windows":
        # Используем встроенный Snipping Tool
        subprocess.run(["snippingtool"])


# Погода

def _cmd_weather(command: str) -> None:
    city = _extract(command, "погода в").strip()
    if not city:
        speak("Назовите город, пожалуйста.")
        return
    info = get_weather(city)
    speak(info)


# Интернет-поиск

def _cmd_search(command: str) -> None:
    # Поддерживаем несколько вариантов фраз
    for kw in ["найди в интернете", "найди", "загугли", "поищи"]:
        if kw in command:
            query = _extract(command, kw)
            break
    else:
        query = ""

    if not query:
        speak("Что именно найти?")
        return

    speak(f"Ищу: {query}.")
    web_search(query)


# YouTube

def _cmd_youtube_open(command: str) -> None:
    speak("Открываю YouTube.")
    open_url("https://www.youtube.com")


def _cmd_youtube_play(command: str) -> None:
    query = _extract(command, "включи видео")
    if not query:
        speak("Что включить?")
        return
    speak(f"Ищу видео: {query}.")
    video_id = get_first_youtube_video_id(query)
    if video_id:
        open_url(f"https://www.youtube.com/watch?v={video_id}")
    else:
        speak("Видео не найдено.")


def _cmd_youtube_search(command: str) -> None:
    query = _extract(command, "найди на ютубе")
    if not query:
        speak("Что искать на YouTube?")
        return
    speak(f"Ищу на YouTube: {query}.")
    encoded_query = query.replace(" ", "+")
    open_url(f"https://www.youtube.com/results?search_query={encoded_query}")


# Сайты и браузер

def _cmd_telegram(command: str) -> None:
    speak("Открываю Telegram.")
    open_url("https://web.telegram.org/")


def _cmd_whatsapp(command: str) -> None:
    speak("Открываю WhatsApp.")
    open_url("https://web.whatsapp.com/")


def _cmd_discord(command: str) -> None:
    speak("Открываю Discord. Хорошего времени!")
    _open_app("Discord")


def _cmd_spotify(command: str) -> None:
    speak("Открываю Spotify.")
    open_url("https://open.spotify.com/")


def _cmd_twitch(command: str) -> None:
    speak("Открываю Twitch.")
    open_url("https://www.twitch.tv/")


def _cmd_github(command: str) -> None:
    speak("Открываю GitHub.")
    open_url("https://github.com")


def _cmd_chatgpt(command: str) -> None:
    speak("Открываю ChatGPT.")
    open_url("https://chat.openai.com")


# Приложения

def _cmd_vscode(command: str) -> None:
    speak("Открываю Visual Studio Code. Удачной работы!")
    _open_app("Visual Studio Code", "code")


def _cmd_obsidian(command: str) -> None:
    speak("Открываю Obsidian.")
    _open_app("Obsidian")


def _cmd_chrome(command: str) -> None:
    speak("Открываю Google Chrome.")
    _open_app("Google Chrome", "chrome")


def _cmd_yandex(command: str) -> None:
    speak("Открываю Яндекс браузер.")
    _open_app("Yandex")


def _cmd_music(command: str) -> None:
    speak("Включаю музыку.")
    _open_app("Music", "wmplayer")


def _cmd_finder(command: str) -> None:
    speak("Открываю Finder.")
    _open_app("Finder", "explorer")


def _cmd_terminal(command: str) -> None:
    speak("Открываю терминал.")
    _open_app("Terminal", "cmd")


def _cmd_calculator(command: str) -> None:
    speak("Открываю калькулятор.")
    _open_app("Calculator")


def _cmd_notes(command: str) -> None:
    speak("Открываю заметки.")
    _open_app("Notes", "notepad")


def _cmd_calendar(command: str) -> None:
    speak("Открываю календарь.")
    _open_app("Calendar")


def _cmd_camera(command: str) -> None:
    speak("Открываю камеру.")
    _open_app("Photo Booth", "Camera")


# ИИ / GPT

def _cmd_ask_ai(command: str) -> None:
    """
    Передаёт вопрос в GPT.
    Срабатывает на: "спроси", "ответь", "объясни", "расскажи", "что такое", "как работает"
    """
    for kw in ["спроси", "ответь", "объясни", "что такое", "как работает", "как называется"]:
        if kw in command:
            question = _extract(command, kw)
            break
    else:
        question = command  # Отдаём всю фразу

    if not question:
        speak("Какой вопрос вас интересует?")
        return

    speak("Думаю...")
    answer = ask_gpt(question)
    speak(answer)


# Wikipedia — быстрый ответ

def _cmd_wiki(command: str) -> None:
    """Ищет объяснение в Wikipedia и озвучивает первые 3 предложения."""
    for kw in ["что такое", "кто такой", "кто такая", "расскажи про", "расскажи о"]:
        if kw in command:
            query = _extract(command, kw)
            break
    else:
        query = command

    if not query:
        speak("Что именно объяснить?")
        return

    speak(f"Ищу информацию о {query}.")
    result = get_wiki_summary(query)

    if result:
        speak(result)
    else:
        speak(f"Не нашёл информацию о {query} в Википедии.")


# Пасхалки / шутки

def _cmd_hack(command: str) -> None:
    speak("Запускаю протокол взлома. Шучу конечно.")


def _cmd_joke(command: str) -> None:
    speak("Расскажи анекдот — сказал Кактус и промолчал.")


#  РОУТЕР КОМАНД
#  Ключ — подстрока в команде, значение — функция

COMMAND_ROUTER: dict[str, callable] = {
    # Время и дата
    "который час":          _cmd_time,
    "сколько время":        _cmd_time,
    "какое время":          _cmd_time,
    "какая сегодня дата":   _cmd_date,
    "какое сегодня число":  _cmd_date,

    # Состояние
    "ты здесь":             _cmd_hello,
    "ты тут":               _cmd_hello,
    "я вернулся":           _cmd_welcome_back,

    # Система
    "выключи компьютер":    _cmd_shutdown,
    "перезагрузи":          _cmd_restart,
    "режим сна":            _cmd_sleep,
    "сделай скриншот":      _cmd_screenshot,
    "скриншот":             _cmd_screenshot,

    # Звук
    "громче":               _cmd_volume_up,
    "увеличь громкость":    _cmd_volume_up,
    "тише":                 _cmd_volume_down,
    "уменьши громкость":    _cmd_volume_down,
    "выключи звук":         _cmd_mute,
    "без звука":            _cmd_mute,

    # Погода
    "погода в":             _cmd_weather,

    # Поиск
    "найди в интернете":    _cmd_search,
    "загугли":              _cmd_search,
    "поищи":                _cmd_search,
    "найди ":               _cmd_search,

    # YouTube
    "открой youtube":       _cmd_youtube_open,
    "открой ютуб":          _cmd_youtube_open,
    "включи видео":         _cmd_youtube_play,
    "найди на ютубе":       _cmd_youtube_search,

    # Сайты
    "открой telegram":      _cmd_telegram,
    "открой телеграм":      _cmd_telegram,
    "открой whatsapp":      _cmd_whatsapp,
    "открой ватсап":        _cmd_whatsapp,
    "открой discord":       _cmd_discord,
    "открой дискорд":       _cmd_discord,
    "открой spotify":       _cmd_spotify,
    "открой спотифай":      _cmd_spotify,
    "открой twitch":        _cmd_twitch,
    "открой твич":          _cmd_twitch,
    "открой github":        _cmd_github,
    "открой гитхаб":        _cmd_github,
    "открой chatgpt":       _cmd_chatgpt,
    "открой чатгпт":        _cmd_chatgpt,

    # Приложения
    "открой проект":        _cmd_vscode,
    "открой vscode":        _cmd_vscode,
    "открой обсидиан":      _cmd_obsidian,
    "включи гугл":          _cmd_chrome,
    "открой хром":          _cmd_chrome,
    "включи яндекс":        _cmd_yandex,
    "включи музыку":        _cmd_music,
    "включи finder":        _cmd_finder,
    "открой файлы":         _cmd_finder,
    "открой терминал":      _cmd_terminal,
    "открой консоль":       _cmd_terminal,
    "открой калькулятор":   _cmd_calculator,
    "открой заметки":       _cmd_notes,
    "открой календарь":     _cmd_calendar,
    "открой камеру":        _cmd_camera,

    # ИИ — вопросы
    "объясни":              _cmd_ask_ai,
    "как работает":         _cmd_ask_ai,
    "как называется":       _cmd_ask_ai,
    "ответь":               _cmd_ask_ai,
    "спроси":               _cmd_ask_ai,

    # Wikipedia
    "что такое":            _cmd_wiki,
    "кто такой":            _cmd_wiki,
    "кто такая":            _cmd_wiki,
    "расскажи про":         _cmd_wiki,
    "расскажи о":           _cmd_wiki,

    # Пасхалки
    "взлом":                _cmd_hack,
    "расскажи анекдот":     _cmd_joke,
}

# Ключевые слова для завершения работы
EXIT_KEYWORDS = {"пока", "стоп", "спасибо", "bye", "выход", "до свидания"}


#  ГЛАВНАЯ ФУНКЦИЯ ОБРАБОТКИ
def process_command(command: str) -> str | None:
    """
    Принимает строку команды, ищет совпадение в роутере и вызывает обработчик.
    Возвращает "exit" если нужно завершить работу, иначе None.
    """

    # Проверка на завершение
    if any(kw in command for kw in EXIT_KEYWORDS):
        speak("К вашим услугам! До встречи.")
        return "exit"

    # Поиск совпадения в роутере (порядок важен — более длинные ключи идут первыми)
    for keyword, handler in COMMAND_ROUTER.items():
        if keyword in command:
            handler(command)
            return None

    # Ничего не нашли — спрашиваем ИИ
    speak("Думаю...")
    answer = ask_gpt(command)
    if answer.startswith("Ошибка") or answer.startswith("Нет соединения") or answer.startswith("ИИ не настроен"):
        print(f"[!] {answer}")
    else:
        speak(answer)

    return None
