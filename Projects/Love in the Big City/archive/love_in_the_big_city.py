import time
import random
import json

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
achievements_list = []
required_skills_for_chapter_2 = 10  # Минимальное количество навыков для перехода к главе 2

# Древо навыков
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

# Вопросы для викторины
questions_pool = [
    {"question": "Какая столица Франции?", "answer": "Париж", "skill": "интеллект"},
    {"question": "Как называется самая большая планета в Солнечной системе?", "answer": "Юпитер", "skill": "интеллект"},
    {"question": "Какой химический элемент обозначается символом 'O'?", "answer": "Кислород", "skill": "интеллект"},
    {"question": "Как называется самая высокая гора в мире?", "answer": "Эверест", "skill": "физическая сила"},
    {"question": "Какой язык программирования чаще всего используется для веб-разработки?", "answer": "JavaScript", "skill": "интеллект"},
    {"question": "Кто написал роман 'Война и мир'?", "answer": "Лев Толстой", "skill": "интеллект"},
    {"question": "Какая планета известна как 'красная планета'?", "answer": "Марс", "skill": "интеллект"},
    {"question": "Какой элемент имеет атомный номер 1?", "answer": "Водород", "skill": "интеллект"},
    {"question": "Как называется самая длинная река в мире?", "answer": "Нил", "skill": "интеллект"},
    {"question": "Кто написал пьесу 'Ромео и Джульетта'?", "answer": "Уильям Шекспир", "skill": "интеллект"}
]

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

# Глобальные переменные для отношений
relationships = {
    "Алекс": 0,
    "Лиза": 0,
    "Макс": 0,
    "Ник": 0,
    "Анна": 0
}

# Глобальные переменные для репутации
location_reputation = {
    "парк": 0,
    "кафе": 0,
    "библиотека": 0,
    "спортивный зал": 0,
    "музей": 0
}

# Глобальная переменная для контента 18+
adult_content_enabled = False

# Глобальные переменные для времени и погоды
current_time = "день"  # Может быть "день" или "ночь"
current_weather = "ясно"  # Может быть "ясно", "дождь", "снег" и т.д.

def start_game():
    global achievements_list
    print("Добро пожаловать в текстовую новеллу 'Love in the Big City'!")
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
        "Привет! Я тоже новенький в городе. Меня зовут Алекс. А тебя?",
        "Здравствуйте! Я Алекс, недавно переехал сюда. А как вас зовут?",
        "Хэй! Я Алекс, новенький в этих краях. А ты кто?"
    ]

    new_friend_name = "Алекс"
    alex_dialogue = random.choice(alex_dialogues)
    print(f"Незнакомец: {alex_dialogue}")

    print(f"Выберите ваш ответ:")
    print("1. Привет, Алекс! Меня зовут {name}. Приятно познакомиться!")
    print("2. Здравствуйте, Алекс. Я {name}. Рад(а) встрече.")
    print("3. Хэй, Алекс! Я {name}. Как тебе город пока?")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        print(f"Алекс: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")
    elif choice == "2":
        print(f"Алекс: Очень приятно, {name}. Может, обменяемся контактами и встретимся снова?")
    elif choice == "3":
        print(f"Алекс: Город пока нравится! Может, обменяемся контактами и встретимся снова, {name}?")
    else:
        print("Вы промолчали и ушли. Возможно, это был не ваш человек.")
        chapter_1(gender, name)
        return

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы обменялись контактами с Алексом и договорились встретиться снова.")
        skills["коммуникабельность"] += 1
        update_relationship("Алекс", 2)
        update_location_reputation("парк", 1)
        quests.append("Встретиться с Алексом в парке")
        check_skills_for_chapter_2(gender, name, new_friend_name, "парк")
    else:
        print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
        update_relationship("Алекс", -1)
        update_location_reputation("парк", -1)
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
            skills["коммуникабельность"] += 1
            update_relationship("Лиза", 2)
            update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это было не ваше место.")
            update_relationship("Лиза", -1)
            update_location_reputation("кафе", -1)
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
            skills["интеллект"] += 1
            update_relationship("Макс", 2)
            update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            update_relationship("Макс", -1)
            update_location_reputation("библиотека", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это был не ваш день.")
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
            skills["физическая сила"] += 1
            update_relationship("Ник", 2)
            update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            update_relationship("Ник", -1)
            update_location_reputation("спортивный зал", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от помощи и продолжаете тренировку самостоятельно. Возможно, это был не ваш день.")
        chapter_1(gender, name)

def museum(gender, name):
    print("\nВы приходите в музей и начинаете осматривать экспонаты.")
    print(f"{name}, вдруг к вам подходит гид и предлагает экскурсию.")
    print("Гид: Привет! Я вижу, ты новенький. Хочешь, проведу экскурсию?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print("Гид проводит для вас увлекательную экскурсию.")
        print("Гид: Надеюсь, тебе понравилось! Меня зовут Анна. А тебя?")

        new_friend_name = "Анна"
        print(f"Вы: Привет, Анна! Меня зовут {name}. Приятно познакомиться!")
        print(f"Анна: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            skills["интеллект"] += 1
            update_relationship("Анна", 2)
            update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            update_relationship("Анна", -1)
            update_location_reputation("музей", -1)
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от экскурсии и продолжаете осмотр самостоятельно. Возможно, это был не ваш день.")
        chapter_1(gender, name)

def city_walk(gender, name):
    print("\nВы решили прогуляться по городу и насладиться его атмосферой.")
    print("Вдруг вы замечаете что-то интересное.")
    print("Вы можете выбрать:")
    print("1. Подойти и рассмотреть.")
    print("2. Продолжить прогулку.")
    print("3. Сделать фотографию.")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        print("Вы подошли и увидели старинную вывеску. Это вызвало у вас интерес.")
        skills["интеллект"] += 1
    elif choice == "2":
        print("Вы продолжили прогулку, наслаждаясь видами города.")
        skills["коммуникабельность"] += 1
    elif choice == "3":
        print("Вы сделали фотографию. Это будет отличный сувенир!")
        skills["харизма"] += 1

    print("Прогулка по городу была приятной и полезной.")
    wait(2)
    main_menu(gender, name)

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    if sum(skills.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    global reputation  # Объявляем переменную как global
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я хотел(а) бы узнать тебя лучше. Может, проведем вместе выходные?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        skills["коммуникабельность"] += 1
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
    print(f"{name} и {new_friend_name} наслаждаются вечером, обсуждая разные темы и узнавая друг друга лучше.")

    # Романтическое событие в ресторане
    print("Вдруг официант приносит вам комплимент от шефа - десерт на выбор!")
    print("Это приятный сюрприз, который делает ваше свидание еще лучше.")
    print("Вы можете выбрать:")
    print("1. Поблагодарить официанта и насладиться десертом.")
    print("2. Предложить разделить десерт с {new_friend_name}.")
    print("3. Попросить упаковать десерт с собой.")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        print(f"Вы поблагодарили официанта и насладились десертом. {new_friend_name} был(а) рад(а) вашему выбору.")
    elif choice == "2":
        print(f"Вы предложили разделить десерт с {new_friend_name}. Это был романтический жест, который укрепил ваши отношения.")
        update_relationship(new_friend_name, 2)
    elif choice == "3":
        print(f"Вы попросили упаковать десерт с собой. {new_friend_name} был(а) удивлен(а), но согласен(а).")

    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
        skills["коммуникабельность"] += 1
        reputation += 1
        chapter_3(gender, name, new_friend_name)
    else:
        print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
        chapter_2(gender, name, new_friend_name, "ресторан")

def park_date(gender, name, new_friend_name):
    print("\nВы гуляете по парку, наслаждаясь природой и компанией друг друга.")
    print(f"{name} и {new_friend_name} садятся на скамейку у озера и разговаривают о жизни и мечтах.")
    print("Вы чувствуете, что между вами возникает романтическое напряжение.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
        skills["коммуникабельность"] += 1
        reputation += 1
        chapter_3(gender, name, new_friend_name)
    else:
        print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
        chapter_2(gender, name, new_friend_name, "парк")

def movie_date(gender, name, new_friend_name):
    print("\nВы идете в кино и смотрите фильм вместе.")
    print(f"{name} и {new_friend_name} обсуждают фильм после просмотра и делятся впечатлениями.")
    print("Вы чувствуете, что между вами возникает романтическое напряжение.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
        skills["коммуникабельность"] += 1
        reputation += 1
        chapter_3(gender, name, new_friend_name)
    else:
        print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
        chapter_2(gender, name, new_friend_name, "кино")

def concert_date(gender, name, new_friend_name):
    print("\nВы идете на концерт и наслаждаетесь музыкой вместе.")
    print(f"{name} и {new_friend_name} танцуют и поют, забывая обо всем вокруг.")
    print("Вы чувствуете, что между вами возникает романтическое напряжение.")
    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
        skills["коммуникабельность"] += 1
        reputation += 1
        chapter_3(gender, name, new_friend_name)
    else:
        print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
        chapter_2(gender, name, new_friend_name, "концерт")

def private_date(gender, name, new_friend_name):
    print("\nВы приходите в уединенное место, где можно насладиться обществом друг друга.")
    print(f"{name} и {new_friend_name} проводят время вместе, наслаждаясь тишиной и уединением.")

    if adult_content_enabled:
        # Эротическое событие
        print("Вы можете выбрать:")
        print("1. Просто насладиться обществом друг друга.")
        print("2. Попробовать что-то более интимное.")
        print("3. Обсудить свои чувства и желания.")

        choice = input("Введите номер выбора: ")
        if choice == "1":
            print(f"Вы просто наслаждаетесь обществом {new_friend_name}. Это был приятный вечер.")
        elif choice == "2":
            print(f"Вы решили попробовать что-то более интимное с {new_friend_name}. Это был особенный момент.")
            update_relationship(new_friend_name, 3)  # Улучшение отношений
        elif choice == "3":
            print(f"Вы обсудили свои чувства и желания с {new_friend_name}. Это укрепило ваши отношения.")
            update_relationship(new_friend_name, 2)
    else:
        print(f"Вы просто наслаждаетесь обществом {new_friend_name}. Это был приятный вечер.")

    print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
        skills["коммуникабельность"] += 1
        reputation += 1
        chapter_3(gender, name, new_friend_name)
    else:
        print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
        chapter_2(gender, name, new_friend_name, "уединенное место")

def chapter_3(gender, name, new_friend_name):
    print("\nГлава 3: Вместе навсегда")
    print(f"Вы нашли свою любовь и построили счастливую жизнь в большом городе.")
    print(f"Вы решаете сделать следующий шаг в ваших отношениях.")
    print(f"{name}, вы делаете предложение и {new_friend_name} соглашается.")
    print("Вы начинаете планировать свадьбу и счастливую жизнь вместе.")
    the_end(gender, name, new_friend_name)

def the_end(gender, name, new_friend_name):
    print("\nКонец")
    print(f"Вы, {name}, нашли свою любовь и построили счастливую жизнь в большом городе с {new_friend_name}.")
    print("Спасибо за игру!")

def wait(seconds):
    time.sleep(seconds)

def random_event(gender, name):
    global reputation, current_time, current_weather

    # Динамические события
    dynamic_events = {
        ("день", "ясно"): ["Вы нашли кошелек на улице.", "Вы встретили старого друга.", "Вы увидели редкую птицу."],
        ("день", "дождь"): ["Вы нашли зонтик на улице.", "Вы помогли кому-то укрыться от дождя.", "Вы нашли потерявшегося котенка."],
        ("ночь", "ясно"): ["Вы увидели падающую звезду.", "Вы встретили ночного гуляку.", "Вы нашли старинную монету."],
        ("ночь", "дождь"): ["Вы помогли кому-то найти дорогу домой.", "Вы нашли потерявшегося щенка.", "Вы увидели таинственный свет."]
    }

    # Редкие события
    rare_events = [
        "Вы нашли древний артефакт на улице.",
        "Вы стали свидетелем НЛО.",
        "Вы встретили знаменитость.",
        "Вы нашли карту сокровищ."
    ]

    # Выбор события
    event = None
    if random.random() < 0.1:  # 10% вероятность редкого события
        event = random.choice(rare_events)
    else:
        event = random.choice(dynamic_events.get((current_time, current_weather), ["Стандартное событие"]))

    print("\nСлучайное событие:")
    print(event)

    if event == "Вы нашли кошелек на улице.":
        print("1. Вернуть кошелек владельцу")
        print("2. Оставить кошелек себе")
        print("3. Отнести кошелек в полицию")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы нашли владельца кошелька и вернули его. Владелец благодарит вас и предлагает дружбу.")
            reputation += 1
            unlock_achievement("Скрытый герой")
        elif choice == "2":
            print("Вы оставили кошелек себе. Возможно, это было не самое честное решение.")
            reputation -= 1
        elif choice == "3":
            print("Вы отнесли кошелек в полицию. Это честное решение, но владелец может и не узнать о вашем поступке.")

    elif event == "Вы нашли карту сокровищ.":
        print("1. Исследовать карту самостоятельно")
        print("2. Поделиться картой с другом")
        print("3. Продать карту коллекционеру")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы решили исследовать карту самостоятельно. Это может привести к приключениям!")
            unlock_achievement("Искатель приключений")
        elif choice == "2":
            print("Вы поделились картой с другом. Вместе вы можете найти сокровище!")
            update_relationship("Алекс", 2)  # Пример улучшения отношений
        elif choice == "3":
            print("Вы продали карту коллекционеру. Это принесло вам прибыль, но вы упустили шанс на приключение.")
            reputation += 1

    wait(2)
    main_menu(gender, name)

def mini_game_puzzle(gender, name):
    print("\nМини-игра: Головоломка")
    print("Решите головоломку, чтобы улучшить свои навыки!")

    # Пример головоломки: анаграмма
    puzzle_word = "лошадь"
    shuffled_word = ''.join(random.sample(puzzle_word, len(puzzle_word)))
    print(f"Переставьте буквы, чтобы составить слово: {shuffled_word}")

    attempts = 3
    while attempts > 0:
        guess = input("Введите ваш ответ: ")
        if guess.lower() == puzzle_word:
            print("Правильно! Вы решили головоломку.")
            skills["интеллект"] += 1
            break
        else:
            attempts -= 1
            print(f"Неправильно! У вас осталось {attempts} попыток.")

    if attempts == 0:
        print(f"К сожалению, вы не смогли решить головоломку. Правильный ответ: {puzzle_word}")

    wait(2)
    main_menu(gender, name)

def show_skills():
    print("\nВаши навыки:")
    for skill, data in skill_tree.items():
        specialization = data["specialization"] if data["specialization"] else "Нет"
        print(f"{skill}: Уровень {data['level']}, Специализация: {specialization}")
    wait(2)

def upgrade_skill(skill):
    if skill in skill_tree:
        skill_tree[skill]["level"] += 1
        print(f"Вы улучшили навык '{skill}' до уровня {skill_tree[skill]['level']}.")

        # Проверка на доступность специализации
        if skill_tree[skill]["level"] >= 5 and skill_tree[skill]["specialization"] is None:
            print(f"Вы разблокировали специализацию для навыка '{skill}'!")
            choose_specialization(skill)

def choose_specialization(skill):
    print(f"Выберите специализацию для навыка '{skill}':")
    for i, spec in enumerate(specializations[skill], 1):
        print(f"{i}. {spec}")

    choice = input("Введите номер выбора: ")
    if choice.isdigit() and 0 < int(choice) <= len(specializations[skill]):
        selected_specialization = specializations[skill][int(choice) - 1]
        skill_tree[skill]["specialization"] = selected_specialization
        print(f"Вы выбрали специализацию '{selected_specialization}' для навыка '{skill}'.")
    else:
        print("Некорректный выбор. Специализация не выбрана.")

def show_quests():
    print("\nВаши квесты:")
    for quest in quests:
        print(f"- {quest}")

    # Добавим побочные квесты
    side_quests = [
        "Помочь старушке донести сумки",
        "Найти потерявшегося котенка",
        "Починить сломанный фонтан в парке"
    ]

    print("\nДоступные побочные квесты:")
    for i, quest in enumerate(side_quests, 1):
        print(f"{i}. {quest}")

    choice = input("Выберите побочный квест для выполнения (или введите 0 для возврата в меню): ")
    if choice.isdigit() and 0 < int(choice) <= len(side_quests):
        selected_quest = side_quests[int(choice) - 1]
        print(f"Вы выбрали квест: {selected_quest}")
        complete_side_quest(selected_quest)
    else:
        main_menu(gender, name)

def complete_side_quest(quest):
    print(f"\nВы выполняете квест: {quest}")

    if quest == "Помочь старушке донести сумки":
        print("Вы помогли старушке и получили в награду домашнее печенье.")
        skills["коммуникабельность"] += 1
    elif quest == "Найти потерявшегося котенка":
        print("Вы нашли котенка и вернули его хозяину. Котенок был очень рад!")
        skills["интеллект"] += 1
    elif quest == "Починить сломанный фонтан в парке":
        print("Вы починили фонтан и жители парка благодарят вас за это.")
        skills["физическая сила"] += 1

    print("Квест выполнен!")
    wait(2)
    main_menu(gender, name)

def show_achievements():
    print("\nВаши достижения:")
    for achievement in achievements_list:
        status = "Достигнуто" if achievement["unlocked"] else "Не достигнуто"
        print(f"- {achievement['name']}: {achievement['description']} ({status})")
    wait(2)

def unlock_achievement(name):
    for achievement in achievements_list:
        if achievement["name"] == name:
            if not achievement["unlocked"]:
                achievement["unlocked"] = True
                print(f"\nДостижение разблокировано: {achievement['name']} - {achievement['description']}")
                apply_reward(achievement["reward"])
            break

def apply_reward(reward):
    if reward == "Бонус к коммуникабельности":
        skills["коммуникабельность"] += 1
    elif reward == "Бонус к харизме":
        skills["харизма"] += 1
    elif reward == "Бонус к интеллекту":
        skills["интеллект"] += 1
    elif reward == "Бонус к физической силе":
        skills["физическая сила"] += 1
    elif reward == "Бонус к удаче":
        skills["удача"] += 1
    elif reward == "Бонус к репутации":
        global reputation
        reputation += 1

def update_relationship(name, points):
    if name in relationships:
        relationships[name] += points
        print(f"Ваши отношения с {name} изменились. Текущий уровень: {relationships[name]}")

        # Уникальные бонусы за высокий уровень отношений
        if relationships[name] >= 10:
            print(f"Вы достигли высокого уровня отношений с {name} и получили уникальный бонус!")
            skills["харизма"] += 1

def update_location_reputation(location, points):
    if location in location_reputation:
        location_reputation[location] += points
        print(f"Ваша репутация в {location} изменилась. Текущий уровень: {location_reputation[location]}")

def save_game(gender, name, slot=1):
    game_state = {
        "name": name,
        "gender": gender,
        "skills": skill_tree,
        "reputation": reputation,
        "location_reputation": location_reputation,
        "relationships": relationships,
        "quests": quests,
        "achievements": achievements_list,
        "current_chapter": "Глава 1"  # Добавьте текущую главу или другую информацию
    }
    with open(f"save_game_slot_{slot}.json", "w") as file:
        json.dump(game_state, file)
    print(f"Игра сохранена в слот {slot}!")

def load_game(slot=1):
    try:
        with open(f"save_game_slot_{slot}.json", "r") as file:
            game_state = json.load(file)
            global name, gender, skill_tree, reputation, location_reputation, relationships, quests, achievements_list
            name = game_state["name"]
            gender = game_state["gender"]
            skill_tree = game_state["skills"]
            reputation = game_state["reputation"]
            location_reputation = game_state["location_reputation"]
            relationships = game_state["relationships"]
            quests = game_state["quests"]
            achievements_list = game_state["achievements"]
            print(f"Игра загружена из слота {slot}!")
            main_menu(gender, name)
    except FileNotFoundError:
        print(f"Сохранение в слоте {slot} не найдено. Начните новую игру.")
        start_game()

def auto_save_game(gender, name):
    save_game(gender, name, slot="auto")
    print("Игра автоматически сохранена!")

def settings_menu():
    print("\nНастройки")
    print("1. Включить/выключить контент 18+")
    print("2. Назад в главное меню")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        toggle_adult_content()
    elif choice == "2":
        main_menu(gender, name)
    else:
        print("Пожалуйста, введите корректный номер.")
        settings_menu()

def toggle_adult_content():
    global adult_content_enabled
    adult_content_enabled = not adult_content_enabled
    status = "включен" if adult_content_enabled else "выключен"
    print(f"Контент 18+ {status}.")

def main_menu(gender, name):
    print("\nГлавное меню")
    print("1. Продолжить игру")
    print("2. Посмотреть навыки")
    print("3. Посмотреть квесты")
    print("4. Посмотреть достижения")
    print("5. Мини-игра")
    print("6. Случайное событие")
    print("7. Сохранить игру")
    print("8. Загрузить игру")
    print("9. Настройки")
    print("10. Выйти из игры")
    print("11. Выбрать слот для сохранения/загрузки")

    choice = input("Введите номер выбора: ")
    if choice == "1":
        chapter_1(gender, name)
    elif choice == "2":
        show_skills()
        main_menu(gender, name)
    elif choice == "3":
        show_quests()
        main_menu(gender, name)
    elif choice == "4":
        show_achievements()
        main_menu(gender, name)
    elif choice == "5":
        mini_game_puzzle(gender, name)
        main_menu(gender, name)
    elif choice == "6":
        random_event(gender, name)
        main_menu(gender, name)
    elif choice == "7":
        slot = int(input("Введите номер слота для сохранения (1-3): "))
        if 1 <= slot <= 3:
            save_game(gender, name, slot)
        else:
            print("Некорректный номер слота.")
        main_menu(gender, name)
    elif choice == "8":
        slot = int(input("Введите номер слота для загрузки (1-3): "))
        if 1 <= slot <= 3:
            load_game(slot)
        else:
            print("Некорректный номер слота.")
    elif choice == "9":
        settings_menu()
    elif choice == "10":
        print("Спасибо за игру! До свидания!")
    elif choice == "11":
        slot_choice = input("Выберите действие: 1 - Сохранить, 2 - Загрузить, 3 - Автосохранение: ")
        if slot_choice == "1":
            slot = int(input("Введите номер слота для сохранения (1-3): "))
            if 1 <= slot <= 3:
                save_game(gender, name, slot)
            else:
                print("Некорректный номер слота.")
        elif slot_choice == "2":
            slot = int(input("Введите номер слота для загрузки (1-3): "))
            if 1 <= slot <= 3:
                load_game(slot)
            else:
                print("Некорректный номер слота.")
        elif slot_choice == "3":
            auto_save_game(gender, name)
        else:
            print("Некорректный выбор.")
        main_menu(gender, name)
    else:
        print("Пожалуйста, введите корректный номер.")
        main_menu(gender, name)

start_game()
