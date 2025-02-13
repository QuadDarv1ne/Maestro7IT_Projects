# Описание проекта - "Любовь в большом городе"

### Основная структура для различных аспектов игры:

1. `quests.py`: для управления квестами.
2. `dialogues.py`: для управления диалогами.
3. `events.py`: для управления событиями.
4. `skills.py`: для управления навыками.
5. `relationships.py`: для управления отношениями.
6. `achievements.py`: для управления достижениями.
7. `save_load.py`: для управления сохранением и загрузкой игры.

```
import time
import random
import json
from quests import manage_quests
from dialogues import manage_dialogues
from events import manage_events
from skills import upgrade_skill, check_skills_for_chapter_2, manage_skills
from relationships import manage_relationships
from achievements import manage_achievements
from save_load import save_game, load_game

# Global variables
skills = {
    "коммуникабельность": 0,
    "интеллект": 0,
    "физическая сила": 0,
    "харизма": 0,
    "удача": 0
}

reputation = 0
quests = []
required_skills_for_chapter_2 = 10  # Minimum skills required to proceed to Chapter 2

# Skill tree
skill_tree = {
    "коммуникабельность": {"level": 0, "specialization": None},
    "интеллект": {"level": 0, "specialization": None},
    "физическая сила": {"level": 0, "specialization": None},
    "харизма": {"level": 0, "specialization": None},
    "удача": {"level": 0, "specialization": None}
}

# Specializations
specializations = {
    "коммуникабельность": ["оратор", "переговорщик"],
    "интеллект": ["аналитик", "исследователь"],
    "физическая сила": ["боец", "спортсмен"],
    "харизма": ["лидер", "общительный"],
    "удача": ["игрок", "авантюрист"]
}

# Achievements
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

# Relationships
relationships = {
    "Алекс": 0,
    "Лиза": 0,
    "Макс": 0,
    "Ник": 0,
    "Анна": 0
}

# Location reputation
location_reputation = {
    "парк": 0,
    "кафе": 0,
    "библиотека": 0,
    "спортивный зал": 0,
    "музей": 0
}

# Adult content flag
adult_content_enabled = False

# Time and weather
current_time = "день"  # Can be "день" or "ночь"
current_weather = "ясно"  # Can be "ясно", "дождь", "снег" etc.

def start_game():
    global achievements_list
    print("Добро пожаловать в текстовую новеллу 'Love in the Big City' :D")
    print("Вы - молодой человек/девушка, который/ая только что переехал/а в большой город.")
    print("Ваша цель - найти свою любовь и построить счастливую жизнь.")

    gender = choose_gender()
    name = input("Введите имя вашего персонажа: ")

    print(f"\nВы выбрали играть за {gender} по имени {name}. Нажмите Enter, чтобы начать ...")
    input()

    achievements_list = [ach for ach in achievements_list]  # Reset achievements
    unlock_achievement("Начало пути")
    main_menu(gender, name)

def choose_gender():
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
    print("\nГлава 1: Новый дом")
    print(f"{name}, вы стоите перед своим новым домом. Куда вы пойдете первым делом?")
    print("1. В парк")
    print("2. В кафе")
    print("3. В библиотеку")
    print("4. В спортивный зал")
    print("5. В музей")
    print("6. На прогулку по городу")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        park(gender, name)
    elif choice == "2":
        cafe(gender, name)
    elif choice == "3":
        library(gender, name)
    elif choice == "4":
        gym(gender, name)
    elif choice == "5":
        museum(gender, name)
    elif choice == "6":
        city_walk(gender, name)
    else:
        print("Пожалуйста, введите корректный номер.")
        chapter_1(gender, name)

def park(gender, name):
    print("\nВы пришли в парк и увидели красивую скамейку у озера.")
    print(f"{name}, вы садитесь и наслаждаетесь видом.")
    print("Вдруг к вам подходит незнакомец и начинает разговор.")

    alex_dialogues = [
        "Привет! Я тоже новенький в городе. Меня зовут Алекс. А тебя?"
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

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Алекс: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")
    elif choice == "2":
        print(f"Алекс: Очень приятно, {name}! Может, обменяемся контактами и встретимся снова?")
    elif choice == "3":
        print(f"Алекс: Город пока нравится! Может, обменяемся контактами и встретимся снова, {name}?")
    else:
        print("Вы промолчали и ушли. Возможно, это был не ваш человек.")
        chapter_1(gender, name)
        return

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы обменялись контактами с Алексом и договорились встретиться снова.")
        manage_skills.upgrade_skill("коммуникабельность")
        manage_relationships.update_relationship("Алекс", 2)
        manage_relationships.update_location_reputation("парк", 1)
        quests.append("Встретиться с Алексом в парке")
        check_skills_for_chapter_2(gender, name, new_friend_name, "парк")
    else:
        print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
        manage_relationships.update_relationship("Алекс", -1)
        manage_relationships.update_location_reputation("парк", -1)
        chapter_1(gender, name)

def cafe(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Макс", 2)
            manage_relationships.update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Макс", -1)
            manage_relationships.update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_relationships.update_relationship("Ник", 2)
            manage_relationships.update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Ник", -1)
            manage_relationships.update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете тренировку самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Анна", 2)
            manage_relationships.update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Анна", -1)
            manage_relationships.update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете осмотр самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
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

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    elif choice == "5":
        private_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Макс", 2)
            manage_relationships.update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Макс", -1)
            manage_relationships.update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_relationships.update_relationship("Ник", 2)
            manage_relationships.update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Ник", -1)
            manage_relationships.update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Анна", 2)
            manage_relationships.update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Анна", -1)
            manage_relationships.update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете осмотр самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
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
        manage_skills.upgrade_skill("коммуникабельность")
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        manage_skills.upgrade_skill("харизма")

    print("Прогулка по городу была приятной и полезной.")
    manage_events.wait(2)
    main_menu(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    elif choice == "5":
        private_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Макс", 2)
            manage_relationships.update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Макс", -1)
            manage_relationships.update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_relationships.update_relationship("Ник", 2)
            manage_relationships.update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Ник", -1)
            manage_relationships.update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Анна", 2)
            manage_relationships.update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Анна", -1)
            manage_relationships.update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
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
        manage_skills.upgrade_skill("коммуникабельность")
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        manage_skills.upgrade_skill("харизма")

    print("Прогулка по городу была приятной и полезной.")
    manage_events.wait(2)
    main_menu(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(a) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    elif choice == "5":
        private_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Макс", 2)
            manage_relationships.update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Макс", -1)
            manage_relationships.update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_relationships.update_relationship("Ник", 2)
            manage_relationships.update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Ник", -1)
            manage_relationships.update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Анна", 2)
            manage_relationships.update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Анна", -1)
            manage_relationships.update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
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
        manage_skills.upgrade_skill("коммуникабельность")
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        manage_skills.upgrade_skill("харизма")

    print("Прогулка по городу была приятной и полезной.")
    manage_events.wait(2)
    main_menu(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(a) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    elif choice == "5":
        private_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def library(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Макс", 2)
            manage_relationships.update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Макс", -1)
            manage_relationships.update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def gym(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_relationships.update_relationship("Ник", 2)
            manage_relationships.update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Ник", -1)
            manage_relationships.update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def museum(gender, name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            upgrade_skill("интеллект")
            manage_relationships.update_relationship("Анна", 2)
            manage_relationships.update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Анна", -1)
            manage_relationships.update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете осмотр самостоятельно. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def city_walk(gender, name):
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
        manage_skills.upgrade_skill("коммуникабельность")
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        manage_skills.upgrade_skill("харизма")

    print("Прогулка по городу была приятной и полезной.")
    manage_events.wait(2)
    main_menu(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def romantic_date(gender, name, new_friend_name):
    print("\nРомантическое свидание")
    print(f"Вы решаете устроить романтическое свидание с {new_friend_name}. Куда вы хотите пойти?")
    print("1. В ресторан")
    print("2. На прогулку по парку")
    print("3. В кино")
    print("4. На концерт")
    print("5. В уединенное место")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    elif choice == "5":
        private_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
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

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_relationships.update_relationship("Лиза", 2)
            manage_relationships.update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_relationships.update_relationship("Лиза", -1)
            manage_relationships.update_location_reputation("кафе", -1)
            chapter_1(gender, name)
    else:
        print("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
        chapter_1(gender, name)

def park_date(gender, name, new_friend_name):
    print("\nВы решили прогуляться по парку с новым знакомым.")
    print(f"{name}, вы наслаждаетесь природой и беседуете.")
    print(f"{new_friend_name}: Это место такое умиротворяющее. Я рад(а), что мы здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете прогулку, наслаждаясь обществом друг друга.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def movie_date(gender, name, new_friend_name):
    print("\nВы решили сходить в кино с новым знакомым.")
    print(f"{name}, вы выбираете фильм и наслаждаетесь просмотром.")
    print(f"{new_friend_name}: Фильм был отличный! Я рад(а), что мы смотрели его вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете обсуждать фильм, наслаждаясь обществом друг друга.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def concert_date(gender, name, new_friend_name):
    print("\nВы решили сходить на концерт с новым знакомым.")
    print(f"{name}, вы наслаждаетесь музыкой и атмосферой.")
    print(f"{new_friend_name}: Концерт был потрясающий! Я рад(а), что мы были здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая концерт.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def private_date(gender, name, new_friend_name):
    print("\nВы решили провести время в уединенном месте с новым знакомым.")
    print(f"{name}, вы наслаждаетесь тишиной и обществом друг друга.")
    print(f"{new_friend_name}: Это место такое спокойное. Я рад(а), что мы здесь вместе.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая разные темы.")
        manage_skills.upgrade_skill("коммуникабельность")
        reputation += 1
        unlock_achievement("Любовь с первого взгляда")
        romantic_date(gender, name, new_friend_name)
    else:
        print(f"Вы вежливо отказываетесь, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def unlock_achievement(achievement_name):
    for achievement in achievements_list:
        if achievement["name"] == achievement_name:
            achievement["unlocked"] = True
            print(f"Достижение разблокировано: {achievement_name}!")
            if achievement["reward"]:
                print(f"Вы получили награду: {achievement['reward']}")
                # Здесь можно добавить логику для применения награды
            break

def main_menu(gender, name):
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
```
