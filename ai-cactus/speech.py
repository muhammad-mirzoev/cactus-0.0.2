#           КАКТУС 0.0.2 - РЕЧЬ
#     Распознавание голоса + синтез речи

import subprocess
import speech_recognition as sr
from config import SPEECH_LANGUAGE, LISTEN_TIMEOUT, LISTEN_PHRASE_LIMIT

# Русский голос macOS - Milena (Premium)
# Другой вариант: "Yuri" - мужской русский голос
VOICE = "yuri"


def speak(text: str) -> None:
    """Произносит текст через встроенную команду macOS say."""
    print(f"[Кактус]: {text}")
    subprocess.run(["say", "-v", VOICE, text])


def listen() -> str:
    """
    Слушает микрофон и возвращает распознанную строку (нижний регистр).
    При ошибке возвращает пустую строку "".
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("\n[Слушаю...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=LISTEN_TIMEOUT,
                phrase_time_limit=LISTEN_PHRASE_LIMIT,
            )
            text = recognizer.recognize_google(audio, language=SPEECH_LANGUAGE)
            print(f"[Ты]: {text}")
            return text.lower().strip()

        except sr.WaitTimeoutError:
            print("[!] Тайм-аут - команда не услышана.")
        except sr.UnknownValueError:
            print("[!] Не удалось распознать речь.")
        except sr.RequestError as e:
            print(f"[!] Ошибка SR: {e}")
            subprocess.run(["say", "-v", VOICE, "Ошибка подключения к сервису распознавания."])
    return ""