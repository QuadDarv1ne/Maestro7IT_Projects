import time
import random
import json

# Глобальные переменные
skills = {"коммуникабельность": 0, "интеллект": 0, "физическая сила": 0, "харизма": 0, "удача": 0}
reputation = 0
quests = []
achievements = []
required_skills_for_chapter_2 = 10  # Минимальное количество навыков для перехода к главе 2

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
    {"name": "Начало пути", "description": "Начать новую игру.", "unlocked": False},
    {"name": "Социальный человек", "description": "Достичь 10 единиц коммуникабельности.", "unlocked": False},
    {"name": "Интеллектуал", "description": "Достичь 10 единиц интеллекта.", "unlocked": False},
    {"name": "Силач", "description": "Достичь 10 единиц физической силы.", "unlocked": False},
    {"name": "Обаятельный", "description": "Достичь 10 единиц харизмы.", "unlocked": False},
    {"name": "Везунчик", "description": "Достичь 10 единиц удачи.", "unlocked": False},
    {"name": "Любовь с первого взгляда", "description": "Успешно завершить первое свидание.", "unlocked": False}
]

def start_game():
    global achievements
    print("Добро пожаловать в текстовую новеллу 'Love in the Big City'!")
    print("Вы - молодой человек/девушка, который/ая только что переехал/а в большой город.")
    print("Ваша цель - найти свою любовь и построить счастливую жизнь.")

    gender = choose_gender()
    name = input("Введите имя вашего персонажа: ")

    print(f"\nВы выбрали играть за {gender} по имени {name}. Нажмите Enter, чтобы начать...")
    input()

    achievements = [ach for ach in achievements_list]  # Сброс достижений
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
    else:
        print("Пожалуйста, введите корректный номер.")
        chapter_1(gender, name)

def park(gender, name):
    print("\nВы пришли в парк и увидели красивую скамейку у озера.")
    print(f"{name}, вы садитесь и наслаждаетесь видом.")
    print("Вдруг к вам подходит незнакомец и начинает разговор.")
    print("Незнакомец: Привет! Я тоже новенький в городе. Меня зовут Алекс. А тебя?")

    new_friend_name = "Алекс"
    print(f"Вы: Привет, Алекс! Меня зовут {name}. Приятно познакомиться!")
    print(f"Алекс: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы обменялись контактами с Алексом и договорились встретиться снова.")
        skills["коммуникабельность"] += 1
        quests.append("Встретиться с Алексом в парке")
        check_skills_for_chapter_2(gender, name, new_friend_name, "парк")
    else:
        print("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
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
            quests.append("Встретиться с Лизой в кафе")
            check_skills_for_chapter_2(gender, name, new_friend_name, "кафе")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это было не ваше место.")
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
            quests.append("Встретиться с Максом в библиотеке")
            check_skills_for_chapter_2(gender, name, new_friend_name, "библиотека")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
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
            quests.append("Встретиться с Ником в спортивном зале")
            check_skills_for_chapter_2(gender, name, new_friend_name, "спортивный зал")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
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
            quests.append("Встретиться с Анной в музее")
            check_skills_for_chapter_2(gender, name, new_friend_name, "музей")
        else:
            print("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            chapter_1(gender, name)
    else:
        print("Вы отказываетесь от экскурсии и продолжаете осмотр самостоятельно. Возможно, это был не ваш день.")
        chapter_1(gender, name)

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

    choice = input("Введите номер выбора: ")
    if choice == "1":
        restaurant_date(gender, name, new_friend_name)
    elif choice == "2":
        park_date(gender, name, new_friend_name)
    elif choice == "3":
        movie_date(gender, name, new_friend_name)
    elif choice == "4":
        concert_date(gender, name, new_friend_name)
    else:
        print("Пожалуйста, введите корректный номер.")
        romantic_date(gender, name, new_friend_name)

def restaurant_date(gender, name, new_friend_name):
    print("\nВы приходите в ресторан и заказываете ужин.")
    print(f"{name} и {new_friend_name} наслаждаются вечером, обсуждая разные темы и узнавая друг друга лучше.")
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
    global reputation  # Объявляем переменную как global
    events = [
        "Вы нашли кошелек на улице. Что вы будете делать?",
        "Вы стали свидетелем ограбления. Что вы будете делать?",
        "Вы получили приглашение на вечеринку. Пойдете ли вы?",
        "Вы встретили старого друга на улице. Что вы будете делать?",
        "Вы встретили привлекательного незнакомца на улице. Что вы будете делать?"
    ]
    event = random.choice(events)
    print("\nСлучайное событие:")
    print(event)

    if event == "Вы нашли кошелек на улице. Что вы будете делать?":
        print("1. Вернуть кошелек владельцу")
        print("2. Оставить кошелек себе")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы нашли владельца кошелька и вернули его. Владелец благодарит вас и предлагает дружбу.")
            reputation += 1
        else:
            print("Вы оставили кошелек себе. Возможно, это было не самое честное решение.")
            reputation -= 1

    elif event == "Вы стали свидетелем ограбления. Что вы будете делать?":
        print("1. Попытаться остановить грабителя")
        print("2. Вызвать полицию")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы попытались остановить грабителя, но он сбежал. Вы герой, но будьте осторожны!")
            skills["физическая сила"] += 1
        else:
            print("Вы вызвали полицию и грабитель был пойман. Вы сделали правильный выбор.")
            reputation += 1

    elif event == "Вы получили приглашение на вечеринку. Пойдете ли вы?":
        print("1. Да, пойду")
        print("2. Нет, не пойду")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы отлично провели время на вечеринке и завели новые знакомства.")
            skills["коммуникабельность"] += 1
        else:
            print("Вы решили остаться дома и отдохнуть. Возможно, это было правильное решение.")

    elif event == "Вы встретили старого друга на улице. Что вы будете делать?":
        print("1. Поговорить и обменяться новостями")
        print("2. Проигнорировать и пройти мимо")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы обменялись новостями и договорились встретиться снова. Приятно вспомнить старые времена.")
            reputation += 1
        else:
            print("Вы проигнорировали старого друга. Возможно, это было не самое вежливое решение.")
            reputation -= 1

    elif event == "Вы встретили привлекательного незнакомца на улице. Что вы будете делать?":
        print("1. Подойти и познакомиться")
        print("2. Проигнорировать и пройти мимо")
        choice = input("Введите номер выбора: ")
        if choice == "1":
            print("Вы подошли и познакомились с незнакомцем. Возможно, это начало нового романа.")
            skills["коммуникабельность"] += 1
        else:
            print("Вы проигнорировали незнакомца. Возможно, это был не самый удачный момент.")

    wait(2)
    main_menu(gender, name)

def mini_game(gender, name):
    print("\nМини-игра: Викторина")
    print("Ответьте на вопросы, чтобы улучшить свои навыки!")

    # Случайный выбор вопросов для викторины
    questions = random.sample(questions_pool, 5)

    for q in questions:
        print(q["question"])
        answer = input("Введите ответ: ")
        if answer.lower() == q["answer"].lower():
            print("Правильно!")
            skills[q["skill"]] += 1
        else:
            print(f"Неправильно! Правильный ответ: {q['answer']}")

    print("Викторина завершена! Ваши навыки улучшены.")
    wait(2)
    main_menu(gender, name)

def show_skills():
    print("\nВаши навыки:")
    for skill, value in skills.items():
        print(f"{skill}: {value}")
    print(f"Репутация: {reputation}")
    wait(2)

def show_quests():
    print("\nВаши квесты:")
    for quest in quests:
        print(f"- {quest}")
    wait(2)

def show_achievements():
    print("\nВаши достижения:")
    for achievement in achievements:
        if achievement["unlocked"]:
            print(f"- {achievement['name']}: {achievement['description']}")
    wait(2)

def unlock_achievement(name):
    for achievement in achievements:
        if achievement["name"] == name:
            achievement["unlocked"] = True
            print(f"\nДостижение разблокировано: {achievement['name']} - {achievement['description']}")
            break

def save_game(gender, name):
    game_state = {
        "name": name,
        "gender": gender,
        "skills": skills,
        "reputation": reputation,
        "quests": quests,
        "achievements": achievements
    }
    with open("save_game.json", "w") as file:
        json.dump(game_state, file)
    print("Игра сохранена!")

def load_game():
    try:
        with open("save_game.json", "r") as file:
            game_state = json.load(file)
            global name, gender, skills, reputation, quests, achievements
            name = game_state["name"]
            gender = game_state["gender"]
            skills = game_state["skills"]
            reputation = game_state["reputation"]
            quests = game_state["quests"]
            achievements = game_state["achievements"]
            print("Игра загружена!")
            main_menu(gender, name)
    except FileNotFoundError:
        print("Сохранение не найдено. Начните новую игру.")
        start_game()

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
    print("9. Выйти из игры")

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
        mini_game(gender, name)
        main_menu(gender, name)
    elif choice == "6":
        random_event(gender, name)
        main_menu(gender, name)
    elif choice == "7":
        save_game(gender, name)
        main_menu(gender, name)
    elif choice == "8":
        load_game()
    elif choice == "9":
        print("Спасибо за игру! До свидания!")
    else:
        print("Пожалуйста, введите корректный номер.")
        main_menu(gender, name)

start_game()
