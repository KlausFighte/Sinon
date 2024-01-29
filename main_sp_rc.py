import speech_recognition as sr
import json
import random
import os
import subprocess
import urllib.parse
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

###################### COLORS ###########################
red_color = '\033[91m'
blue_color = '\033[94m'
end_color = '\033[0m'
#########################################################

def load_database(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        database = json.load(file)
    return database

#######################################################  обработка команд  ############################################################

def process_command(command, database):
    command = command.lower()
    # пошук відповідної команди за ключовими словами
    for key, keywords in database.items():
        for keyword in keywords:
            if keyword.lower() in command:

                responses = {
                    "Hello": ["Привіт!", "Привіт-привіт!", "Привітствую вас!"],
                    "Goodbye": ["До побачення!", "Пока!", "Гарного дня!"],
                    "Search": ["Шукаю...", "Пошук в процесі...", "Ваш запит обробляється..."],
                    "set volume": [f"Гучність була виставленна на%", f"гучніть успішно виставленна на %"],
                    "open website": ["Відкриваю веб-сайт. Зачекайте трошки...", "Переходимо за посиланням...", "Ваш сайт відкривається..."],
                    "How are you": ["Все добре, дякую!", "Дуже добре, спасибі!", "Чудово!"],
                    "What's your name": ["Мене звуть Голосовий Помічник!", "Я ваш асистент!", "Ви можете звати мене Асистент!"],
                    "Tell a joke": ["Чому програміст завжди холодно? Бо завжди є Windows!", "Що робить баг? Живе в коді!", "Як ви перевіряєте шукача багів? Питаєте: 'Це не баг, це фіча?'"],
                    "Weather": ["Прогноз погоди: Сонячно!", "Погода зараз: 25 градусів Цельсія!", "Погода на завтра: Тепло і сонячно!"],
                    "Time": ["Поточний час: 12:30 PM", "Скільки годин? 3:45 PM", "Зараз час вказує 11 годин 20 хвилин."],
                    "Play music": ["Відтворюю улюблену пісню!", "Насолоджуйтесь музикою!", "Обирайте свою улюблену мелодію!"],
                    "Open website": ["Відкриваю веб-сайт. Зачекайте трошки...", "Переходимо за посиланням..."],
                    "What is your purpose": ["Моя мета - допомагати вам!", "Я тут, щоб вас підтримувати!", "Моя ціль - зробити ваш день кращим!"],
                    "Translate": ["Перекладаю ваш текст...", "Мова - це не перешкода для мене!", "Ваш текст на іншій мові: ..."],
                    "Remind me": ["Запам'ятовую ваше прохання!", "Буду нагадувати вам вчасно!", "Нагадаю про це пізніше!"],
                    "Tell a story": ["Є одна цікава історія...", "Станете слухачем? Почнемо історію!", "Жили-були..."],
                    "Send email": ["Відправляю електронний лист...", "Починаю процес відправлення листа...", "Лист в дорозі до отримувача!"],
                    "Tell me a fact": ["Оцікавте факт: ...", "Факт: ...", "Цікавий факт для вас: ..."],
                    "Recommend a movie": ["Рекомендую глянути фільм: ...", "Фільм для перегляду: ...", "Мій вибір: ..."],
                    "What's the meaning of life": ["Смисл життя - це існувати в добро і робити світ кращим!", "Життя - це шлях до власного щастя і щастя інших.", "Смисл життя полягає в тому, щоб вчитися, рости та любити."],
                    "Sing a song": ["Ла-ла-ла, співаю для вас!", "Ваш улюблений хіт в виконанні Голосового Помічника!", "Мелодія летить у вашу сторону..."],
                    "Who is your favorite superhero": ["Мій улюблений супергерой - той, хто здатен допомагати всім!", "Супергерой, який принесе світло і добро.", "Мій улюблений супергерой - кожен, хто робить світ кращим!"],
                    "Tell me a fun fact about yourself": ["Цікавий факт: я вивчаю нові речі щоденно!", "Факт про мене: я завжди тут, щоб допомагати!", "Розвага для вас: я вчуся від користувачів кожного дня!"],
                    "Google search": ["ищу", "вже шукаю", "виконую"],
                }

                if key == "set volume":
                    try:
                        volume_percent = int(''.join(filter(str.isdigit, command)))
                        volume_percent = max(0, min(volume_percent, 100))
                        set_volume(volume_percent)
                        print(f"Гучність встановлено на {volume_percent}%")
                    except ValueError:
                        print("Не вдалося визначити відсоток гучності")



                elif key == "Play music":
                    play_music()
                    return {key: "Відтворюю музику на Spotify!"}

                elif key == "open website":     # Отримайте URL веб-сайту з команди, наприклад, "відкрий веб-сайт example.com"
                    website_url = command.replace(keyword.lower(), "").strip()
                    open_website(website_url)
                    print(f"Відкриваю веб-сайт: {website_url}")

                elif key == "Google search":
                    try:
                        query = command.split(' ', 2)[2]
                        result = google_search(query)
                        if result:
                            return {key: result}
                        else:
                            return "Не вдалося виконати пошук"

                    except IndexError:
                        print("Не вказано запит для пошуку")
                        return



                response = random.choice(responses[key])
                print(f"{red_color}{response}{end_color}")

                return {key: keywords}

    return "Не знайдено відповідної команди"

#==================================================== Дефи команд====================================================================#

def google_search(query):
    try:
        result = next(google_search(query, num_results=1))
        return result
    except StopIteration:
        return None

def set_volume(volume_percent):
    script = f"set volume output volume {volume_percent}" # встановлює гучність на macOS
    os.system(f"osascript -e '{script}'")

def open_website(website_url):
    if "google.com" in website_url or "youtube.com" in website_url:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            if "google.com" in website_url:
                print("Що ви хочете знайти на Google?")
            elif "youtube.com" in website_url:
                print("Що ви хочете знайти на YouTube?")

            audio = recognizer.listen(source)

        try:
            search_query = recognizer.recognize_google(audio, language="uk-UA")
            print(f"Ваш запит: {search_query}")

            if "google.com" in website_url:
                search_url = f"{website_url}/search?q={urllib.parse.quote(search_query)}"
            elif "youtube.com" in website_url:
                search_url = f"{website_url}/results?search_query={urllib.parse.quote(search_query)}"

            subprocess.run(["open", search_url])
            print(f"Виконую пошук на {website_url}.")
        except sr.UnknownValueError:
            print("Не розпізнано голос")
    else:
        subprocess.run(["open", website_url])
        print(f"Відкриваю веб-сайт: {website_url}")

def play_music():
    # Використовуйте правильний URL-схему для Spotify
    spotify_url_scheme = "spotify:"
    subprocess.run(["open", spotify_url_scheme])
    print("Відтворюю музику на Spotify.")
##############################################################################################################################################
def execute_commands(audio, database):
    recognizer = sr.Recognizer()
    try:
        commands = recognizer.recognize_google(audio, language="uk-UA", show_all=True)
        for result in commands.get("alternative", []):
            command = result["transcript"]
            print(f"Ви сказали: {blue_color}{command}{end_color}")
            process_result = process_command(command, database)
            print(process_result)

    except sr.UnknownValueError:
        print("Не розпізнано голос")

def main():
    recognizer = sr.Recognizer()
    database_file = "database.json"
    database = load_database(database_file)

    while True:
        with sr.Microphone() as source:
            print("Скажіть команду:")
            audio = recognizer.listen(source)

        execute_commands(audio, database)

if __name__ == "__main__":
    main()


#//by.Klaus :з
