import random
import time
import json
import logging
from config import EVENT_PROBABILITIES, EVENTS
from quests import manage_quests
from dialogues import manage_dialogues
from events import manage_events
from skills import upgrade_skill, check_skills_for_chapter_2, manage_skills
from relationships import manage_relationships
from achievements import manage_achievements
from save_load import save_game, load_game

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="game.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Глобальные переменные
skills = {
    "коммуникабельность": 0,
    "интеллект": 0,
    "физическая сила": 0,
    "харизма": 0,
    "удача": 0
}

reputation = 0
quests = []
required_skills_for_chapter_2 = 10  # Минимальные навыки для перехода ко второй главе

# Дерево навыков
skill_tree = {
    "коммуникабельность": {"level": 0, "specialization": None},
    "интеллект": {"level": 0, "specialization": None},
    "физическая сила": {"level": 0, "specialization": None},
    "харизма": {"level": 0, "specialization": None},
    "удача": {"level": 0, "specialization": None}
}

# Специализации
specializations = {
    "коммуникабельность": ["оратор", "переговорщик"],
    "интеллект": ["аналитик", "исследователь"],
    "физическая сила": ["боец", "спортсмен"],
    "харизма": ["лидер", "общительный"],
    "удача": ["игрок", "авантюрист"]
}

# Достижения
achievements_list = [
    {"name": "Начало пути", "description": "Начать новую игру.", "unlocked": False, "reward": "Бонус к коммуникабельности"},
    {"name": "Социальный человек", "description": "Достичь 10 единиц коммуникабельности.", "unlocked": False, "reward": "Бонус к харизме"},
    {"name": "Интеллектуал", "description": "Достичь 10 единиц интеллекта.", "unlocked": False, "reward": "Бонус к интеллекту"},
    {"name": "Силач", "description": "Достичь 10 единиц физической силы.", "unlocked": False, "reward": "Бонус к физической силе"},
    {"name": "Обаятельный", "description": "Достичь 10 единиц харизмы.", "unlocked": False, "reward": "Бонус к харизме"},
    {"name": "Везунчик", "description": "Достичь 10 единиц удачи.", "unlocked": False, "reward": "Бонус к удаче"},
    {"name": "Любовь с первого взгляда", "description": "Успешно завершить первое свидание.", "unlocked": False, "reward": "Бонус к коммуникабельности"},
    {"name": "Скрытый герой", "description": "Вернуть потерянный кошелек владельцу.", "unlocked": False, "reward": "Бонус к репутации"},
    {"name": "Детектив", "description": "Раскрыть преступление и помочь полиции.", "unlocked": False, "reward": "Бонус к интеллекту"}
]

# Отношения
relationships = {
    "Алекс": 0,
    "Лиза": 0,
    "Макс": 0,
    "Ник": 0,
    "Анна": 0
}

# Репутация локаций
location_reputation = {
    "парк": 0,
    "кафе": 0,
    "библиотека": 0,
    "спортивный зал": 0,
    "музей": 0
}

# Включение контента для взрослых
adult_content_enabled = False

# Время и погода
current_time = "день"  # Может быть "день" или "ночь"
current_weather = "ясно"  # Может быть "ясно", "дождь", "снег" и т.д.

def start_game():
    """Начало игры."""
    global achievements_list
    print("Добро пожаловать в текстовую новеллу 'Love in the Big City' :D")
    print("Вы - молодой человек/девушка, который/ая только что переехал/а в большой город.")
    print("Ваша цель - найти свою любовь и построить счастливую жизнь.")

    gender = choose_gender()
    name = input("Введите имя вашего персонажа: ")

    print(f"\nВы выбрали играть за {gender} по имени {name}. Нажмите Enter, чтобы начать...")
    input()

    achievements_list = [ach for ach in achievements_list]  # Сброс достижений
    unlock_achievement("Начало пути")
    main_menu(gender, name)

def choose_gender():
    """Выбор пола персонажа."""
    print("\nВыберите пол вашего персонажа:")
    print("1. Мужчина")
    print("2. Женщина")

    gender_choice = input("Введите номер выбора: ")
    if gender_choice == "1":
        return "мужчина"
    elif gender_choice == "2":
        return "женщина"
    else:
        print("Пожалуйста, введите корректный номер.")
        return choose_gender()

def chapter_1(gender, name):
    """Глава 1: Новый дом."""
    print("\nГлава 1: Новый дом")
    print(f"{name}, вы стоите перед своим новым домом. Куда вы пойдете первым делом?")
    print("1. В парк")
    print("2. В кафе")
    print("3. В библиотеку")
    print("4. В спортивный зал")
    print("5. В музей")
    print("6. На прогулку по городу")

    choice = input("Введите номер выбора: ")
    location_actions = {
        "1": park,
        "2": cafe,
        "3": library,
        "4": gym,
        "5": museum,
        "6": city_walk
    }
    action = location_actions.get(choice)
    if action:
        action(gender, name)
    else:
        print("Пожалуйста, введите корректный номер.")
        chapter_1(gender, name)

def park(gender, name):
    """Действия в парке."""
    print("\nВы пришли в парк и увидели красивую скамейку у озера.")
    print(f"{name}, вы садитесь и наслаждаетесь видом.")
    print("Вдруг к вам подходит незнакомец и начинает разговор.")

    alex_dialogues = [
        "Привет! Я тоже новенький в городе. Меня зовут Алекс. А тебя?",
        "Здравствуйте! Я Алекс, недавно переехал сюда. А как вас зовут?",
        "Хэй! Я Алекс, новенький в этих краях. А ты кто?"
    ]

    new_friend_name = "Алекс"
    alex_dialogue = random.choice(alex_dialogues)
    print(f"Незнакомец: {alex_dialogue}")

    print(f"Выберите ваш ответ:")
    print("1. Привет, Алекс! Меня зовут {name}. Приятно познакомиться!")
    print("2. Здравствуйте! Я Алекс. А тебя?")
    print("3. Хэй, Алекс! Я {name}. Как тебе город пока?")

    handle_new_friend_interaction(gender, name, new_friend_name, "парк")

def cafe(gender, name):
    """Действия в кафе."""
    print("\nВы приходите в уютное кафе и заказываете кофе.")
    print(f"{name}, пока вы ждете заказ, к вам подходит официант и предлагает попробовать новый десерт.")
    print("Официант: Привет! Я вижу, ты новенький. Хочешь попробовать наш новый десерт?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Вы пробуете десерт и он оказывается восхитительным. Официант рад вашей реакции.")
        print("Официант: Рад, что тебе понравилось! Меня зовут Лиза. А тебя?")

        new_friend_name = "Лиза"
        print(f"Вы: Привет, Лиза! Меня зовут {name}. Приятно познакомиться!")
        print(f"Лиза: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        handle_new_friend_interaction(gender, name, new_friend_name, "кафе")
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
    """Действия в библиотеке."""
    print("\nВы приходите в библиотеку и начинаете искать интересную книгу.")
    print(f"{name}, вдруг к вам подходит библиотекарь и предлагает помощь.")
    print("Библиотекарь: Привет! Я вижу, ты новенький. Могу помочь найти интересную книгу?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Библиотекарь помогает вам найти отличную книгу.")
        print("Библиотекарь: Надеюсь, тебе понравится! Меня зовут Макс. А тебя?")

        new_friend_name = "Макс"
        print(f"Вы: Привет, Макс! Меня зовут {name}. Приятно познакомиться!")
        print(f"Макс: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        handle_new_friend_interaction(gender, name, new_friend_name, "библиотека")
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
    """Действия в спортивном зале."""
    print("\nВы приходите в спортивный зал и начинаете тренировку.")
    print(f"{name}, вдруг к вам подходит тренер и предлагает помощь.")
    print("Тренер: Привет! Я вижу, ты новенький. Хочешь, помогу с тренировкой?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Тренер помогает вам с тренировкой и дает полезные советы.")
        print("Тренер: Отличная работа! Меня зовут Ник. А тебя?")

        new_friend_name = "Ник"
        print(f"Вы: Привет, Ник! Меня зовут {name}. Приятно познакомиться!")
        print(f"Ник: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        handle_new_friend_interaction(gender, name, new_friend_name, "спортивный зал")
    else:
        print("Вы отказываетесь от помощи и продолжаете тренировку самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
    """Действия в музее."""
    print("\nВы приходите в музей и начинаете осматривать экспонаты.")
    print(f"{name}, вдруг к вам подходит гид и предлагает экскурсию.")
    print("Гид: Привет! Я вижу, ты новенький. Хочешь, проведу экскурсию?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Гид проводит для вас увлекательную экскурсию.")
        print("Гид: Надеюсь, тебе понравится! Меня зовут Анна. А тебя?")

        new_friend_name = "Анна"
        print(f"Вы: Привет, Анна! Меня зовут {name}. Приятно познакомиться!")
        print(f"Анна: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        handle_new_friend_interaction(gender, name, new_friend_name, "музей")
    else:
        print("Вы отказываетесь от помощи и продолжаете осмотр самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
    """Прогулка по городу."""
    print("\nВы решили прогуляться по городу и наслаждаетесь его атмосферой.")
    print("Вдруг вы замечаете что-то интересное.")
    print("Вы можете выбрать:")
    print("1. Подойти и рассмотреть.")
    print("2. Продолжить прогулку.")
    print("3. Сделать фотографию.")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        print("Вы подошли и увидели старинную вывеску. Это вызвало у вас интерес.")
        upgrade_skill("интеллект")
    elif choice == "2":
        print("Вы продолжили прогулку, наслаждаясь видами города.")
        upgrade_skill("коммуникабельность")
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        upgrade_skill("харизма")

    print("Прогулка по городу была приятной и полезной.")
    manage_events.wait(2)
    main_menu(gender, name)

def handle_new_friend_interaction(gender, name, new_friend_name, location):
    """Обработка взаимодействия с новым другом."""
    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы обменялись контактами с {new_friend_name} и договорились встретиться снова.")
        upgrade_skill("коммуникабельность")
        manage_relationships.update_relationship(new_friend_name, 2)
        manage_relationships.update_location_reputation(location, 1)
        quests.append(f"Встретиться с {new_friend_name} в {location}")
        check_skills_for_chapter_2(gender, name, new_friend_name, location)
    else:
        print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
        manage_relationships.update_relationship(new_friend_name, -1)
        manage_relationships.update_location_reputation(location, -1)
        chapter_1(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    """Проверка навыков для перехода ко второй главе."""
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    """Глава 2: Новые знакомства."""
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    """Романтическое свидание."""
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    date_actions = {
        "1": restaurant_date,
        "2": park_date,
        "3": movie_date,
        "4": concert_date,
        "5": private_date
    }
    action = date_actions.get(choice)
    if action:
        action(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
    """Свидание в ресторане."""
    print("\nВы приходите в ресторан и заказываете ужин.")
    print(f"{name}, пока вы ждете заказ, к вам подходит официант и предлагает попробовать новый десерт.")
    print("Официант: Привет! Я вижу, ты новенький. Хочешь попробовать наш новый десерт?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Вы пробуете десерт и он оказывается восхитительным. Официант рад вашей реакции.")
        print("Официант: Рад, что тебе понравилось! Меня зовут Лиза. А тебя?")

        new_friend_name = "Лиза"
        print(f"Вы: Привет, Лиза! Меня зовут {name}. Приятно познакомиться!")
        print(f"Лиза: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        handle_new_friend_interaction(gender, name, new_friend_name, "кафе")
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def park_date(gender, name, new_friend_name):
    """Свидание в парке."""
    print("\nВы решили прогуляться по парку с новым знакомым.")
    print(f"{name}, вы наслаждаетесь природой и беседуете.")
    print(f"{new_friend_name}: Это место такое умиротворяющее. Я рад(а), что мы здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете прогулку, наслаждаясь обществом друг друга.")
        upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, "парк")

def movie_date(gender, name, new_friend_name):
    """Свидание в кино."""
    print("\nВы решили сходить в кино с новым знакомым.")
    print(f"{name}, вы выбираете фильм и наслаждаетесь просмотром.")
    print(f"{new_friend_name}: Фильм был отличный! Я рад(а), что мы смотрели его вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете обсуждать фильм, наслаждаясь обществом друг друга.")
        upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, "кино")

def concert_date(gender, name, new_friend_name):
    """Свидание на концерте."""
    print("\nВы решили сходить на концерт с новым знакомым.")
    print(f"{name}, вы наслаждаетесь музыкой и атмосферой.")
    print(f"{new_friend_name}: Концерт был потрясающий! Я рад(а), что мы были здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая концерт.")
        upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, "концерт")

def private_date(gender, name, new_friend_name):
    """Свидание в уединенном месте."""
    print("\nВы решили провести время в уединенном месте с новым знакомым.")
    print(f"{name}, вы наслаждаетесь тишиной и обществом друг друга.")
    print(f"{new_friend_name}: Это место такое спокойное. Я рад(а), что мы здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая разные темы.")
        upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, "уединенное место")

def unlock_achievement(achievement_name):
    """Разблокировка достижения."""
    for achievement in achievements_list:
        if achievement["name"] == achievement_name:
            achievement["unlocked"] = True
            print(f"Достижение разблокировано: {achievement_name}!")
            if achievement["reward"]:
                print(f"Вы получили награду: {achievement['reward']}")
                # Здесь можно добавить логику для применения награды
            break

def main_menu(gender, name):
    """Главное меню."""
    print("\nГлавное меню")
    print("1. Продолжить игру")
    print("2. Сохранить игру")
    print("3. Загрузить игру")
    print("4. Выйти из игры")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        chapter_1(gender, name)
    elif choice == "2":
        save_game(gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list)
        print("Игра сохранена!")
        main_menu(gender, name)
    elif choice == "3":
        gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list = load_game()
        print("Игра загружена!")
        main_menu(gender, name)
    elif choice == "4":
        print("Спасибо за игру! До новых встреч!")
    else:
        print("Пожалуйста, введите корректный номер.")
        main_menu(gender, name)

def save_game(gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list):
    """Сохранение игры."""
    game_data = {
        "gender": gender,
        "name": name,
        "skills": skills,
        "reputation": reputation,
        "quests": quests,
        "relationships": relationships,
        "location_reputation": location_reputation,
        "achievements_list": achievements_list
    }
    with open("save_game.json", "w") as file:
        json.dump(game_data, file)

def load_game():
    """Загрузка игры."""
    with open("save_game.json", "r") as file:
        game_data = json.load(file)
    return (
        game_data["gender"],
        game_data["name"],
        game_data["skills"],
        game_data["reputation"],
        game_data["quests"],
        game_data["relationships"],
        game_data["location_reputation"],
        game_data["achievements_list"]
    )

if __name__ == "__main__":
    start_game()
