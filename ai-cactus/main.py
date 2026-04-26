from speech import speak, listen
from commands import process_command

BANNER = """
╔══════════════════════════════════════════╗
║   🌵  КАКТУС v0.0.2  -  Голосовой ИИ   ║
║   Скажи "пока" или нажми Ctrl+C         ║
╚══════════════════════════════════════════╝
"""


def run_cactus() -> None:
    print(BANNER)
    speak("Здравствуйте, я Кактус версия ноль точка ноль два. Чем могу помочь?")

    try:
        while True:
            command = listen()

            # Пустая строка - ничего не услышали, продолжаем слушать
            if not command:
                continue

            result = process_command(command)

            if result == "exit":
                break

    except KeyboardInterrupt:
        speak("До свидания!")
        print("\n[Выход из программы]")


if __name__ == "__main__":
    run_cactus()
