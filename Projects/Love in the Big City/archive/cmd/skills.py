# skills.py

skill_tree = {
    "коммуникабельность": {"level": 0, "specialization": None},
    "интеллект": {"level": 0, "specialization": None},
    "физическая сила": {"level": 0, "specialization": None},
    "харизма": {"level": 0, "specialization": None},
    "удача": {"level": 0, "specialization": None}
}

specializations = {
    "коммуникабельность": ["оратор", "переговорщик"],
    "интеллект": ["аналитик", "исследователь"],
    "физическая сила": ["боец", "спортсмен"],
    "харизма": ["лидер", "общительный"],
    "удача": ["игрок", "авантюрист"]
}

def upgrade_skill(skill):
    if skill in skill_tree:
        skill_tree[skill]["level"] += 1
        print(f"Вы улучшили навык '{skill}' до уровня {skill_tree[skill]['level']}.")

        if skill_tree[skill]["level"] >= 5 and skill_tree[skill]["specialization"] is None:
            print(f"Вы разблокировали специализацию для навыка '{skill}'!")
            choose_specialization(skill)

def choose_specialization(skill):
    print(f"Выберите специализацию для навыка '{skill}':")
    for idx, spec in enumerate(specializations[skill], start=1):
        print(f"{idx}. {spec}")

    choice = int(input("Введите номер выбора: ")) - 1
    if 0 <= choice < len(specializations[skill]):
        skill_tree[skill]["specialization"] = specializations[skill][choice]
        print(f"Вы выбрали специализацию '{specializations[skill][choice]}' для навыка '{skill}'.")
    else:
        print("Некорректный выбор. Специализация не выбрана.")

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    required_skills_for_chapter_2 = 10
    if sum(skill["level"] for skill in skill_tree.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skill['level'] for skill in skill_tree.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    global reputation
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я хотел(а) бы узнать тебя лучше. Может, проведем вместе выходные?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        upgrade_skill("коммуникабельность")
        update_relationship(new_friend_name, 2)
        update_location_reputation(location, 1)
        add_quest(f"Встретиться с {new_friend_name} в {location}")
        check_skills_for_chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вы вежливо отказались, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

# skills.py

skill_tree = {
    "коммуникабельность": {"level": 0, "specialization": None},
    "интеллект": {"level": 0, "specialization": None},
    "физическая сила": {"level": 0, "specialization": None},
    "харизма": {"level": 0, "specialization": None},
    "удача": {"level": 0, "specialization": None}
}

specializations = {
    "коммуникабельность": ["оратор", "переговорщик"],
    "интеллект": ["аналитик", "исследователь"],
    "физическая сила": ["боец", "спортсмен"],
    "харизма": ["лидер", "общительный"],
    "удача": ["игрок", "авантюрист"]
}

def upgrade_skill(skill):
    if skill in skill_tree:
        skill_tree[skill]["level"] += 1
        print(f"Вы улучшили навык '{skill}' до уровня {skill_tree[skill]['level']}.")

        if skill_tree[skill]["level"] >= 5 and skill_tree[skill]["specialization"] is None:
            print(f"Вы разблокировали специализацию для навыка '{skill}'!")
            choose_specialization(skill)

def choose_specialization(skill):
    print(f"Выберите специализацию для навыка '{skill}':")
    for idx, spec in enumerate(specializations[skill], start=1):
        print(f"{idx}. {spec}")

    choice = int(input("Введите номер выбора: ")) - 1
    if 0 <= choice < len(specializations[skill]):
        skill_tree[skill]["specialization"] = specializations[skill][choice]
        print(f"Вы выбрали специализацию '{specializations[skill][choice]}' для навыка '{skill}'.")
    else:
        print("Некорректный выбор. Специализация не выбрана.")

def check_skills_for_chapter_2(gender, name, new_friend_name, location):
    required_skills_for_chapter_2 = 10
    if sum(skill["level"] for skill in skill_tree.values()) >= required_skills_for_chapter_2:
        chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skill['level'] for skill in skill_tree.values())} навыков, чтобы перейти к следующей главе.")
        main_menu(gender, name)

def chapter_2(gender, name, new_friend_name, location):
    global reputation
    print("\nГлава 2: Новые знакомства")
    print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
    print(f"Вы чувствуете, что между вами возникает что-то особенное.")
    print(f"{new_friend_name}: {name}, я хотел(а) бы узнать тебя лучше. Может, проведем вместе выходные?")

    choice = input("Введите 'да' или 'нет': ").lower()
    if choice == "да":
        print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
        upgrade_skill("коммуникабельность")
        update_relationship(new_friend_name, 2)
        update_location_reputation(location, 1)
        add_quest(f"Встретиться с {new_friend_name} в {location}")
        check_skills_for_chapter_2(gender, name, new_friend_name, location)
    else:
        print(f"Вы вежливо отказались, но {new_friend_name} не сдается и предлагает встретиться позже.")
        chapter_2(gender, name, new_friend_name, location)

def manage_skills():
    # Эта функция может содержать логику для управления навыками, например, вывод текущих навыков и их уровней
    print("Управление навыками:")
    for skill, details in skill_tree.items():
        level = details["level"]
        specialization = details["specialization"]
        print(f"{skill}: Уровень {level}, Специализация: {specialization if specialization else 'Нет'}")
