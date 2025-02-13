# Управление навыками

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

def manage_skills():
    global skill_tree, specializations

    # Пример функции для улучшения навыка
    def upgrade_skill(skill):
        if skill in skill_tree:
            skill_tree[skill]["level"] += 1
            print(f"Вы улучшили навык '{skill}' до уровня {skill_tree[skill]['level']}.")

            # Проверка на доступность специализации
            if skill_tree[skill]["level"] >= 5 and skill_tree[skill]["specialization"] is None:
                print(f"Вы разблокировали специализацию для навыка '{skill}'!")
                choose_specialization(skill)

    # Пример функции для проверки навыков для перехода к главе 2
    def check_skills_for_chapter_2(gender, name, new_friend_name, location):
        if sum(skill_tree.values()) >= required_skills_for_chapter_2:
            chapter_2(gender, name, new_friend_name, location)
        else:
            print(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skill_tree.values())} навыков, чтобы перейти к следующей главе.")
            main_menu(gender, name)

    # Пример функции для перехода к главе 2
    def chapter_2(gender, name, new_friend_name, location):
        global reputation
        print("\nГлава 2: Новые знакомства")
        print(f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.")
        print(f"Вы чувствуете, что между вами возникает что-то особенное.")
        print(f"{new_friend_name}: {name}, я хотел(а) бы узнать тебя лучше. Может, проведем вместе выходные?")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы соглашаетесь и проводите выходные с {new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation(location, 1)
            manage_quests.add_quest(f"Встретиться с {new_friend_name} в {location}")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, location)
        else:
            print(f"Вы вежливо отказались, но {new_friend_name} не сдается и предлагает встретиться позже.")
            chapter_2(gender, name, new_friend_name, location)

    # Пример функции для перехода к главе 3
    def chapter_3(gender, name, new_friend_name):
        print("\nГлава 3: Вместе навсегда")
        print(f"Вы нашли свою любовь и построили счастливую жизнь в большом городе.")
        print(f"Вы решаете сделать следующий шаг в ваших отношениях.")
        print(f"{name}, вы делаете предложение и {new_friend_name} соглашается.")
        print("Вы начинаете планировать свадьбу и счастливую жизнь вместе.")
        manage_achievements.the_end(gender, name, new_friend_name)
