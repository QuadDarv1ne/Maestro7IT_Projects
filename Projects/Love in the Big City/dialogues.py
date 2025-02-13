# Управление диалогами

def manage_dialogues():
    # Пример функции для выбора диалога
    def choose_dialogue(options):
        choice = input("Введите номер выбора: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("Пожалуйста, введите корректный номер.")
            return choose_dialogue(options)

    # Пример функции для романтического свидания
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

    # Пример функции для свидания в ресторане
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
            manage_skills.upgrade_skill("коммуникабельность")
        elif choice == "3":
            print(f"Вы попросили упаковать десерт с собой. {new_friend_name} был(а) удивлен(а), но согласен(а).")

        print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation("ресторан", 1)
            quests.append("Встретиться с {new_friend_name} в ресторане")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, "ресторан")
        else:
            print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
            manage_skills.chapter_2(gender, name, new_friend_name, "ресторан")

    # Пример функции для свидания в парке
    def park_date(gender, name, new_friend_name):
        print("\nВы гуляете по парку, наслаждаясь природой и обществом друг друга.")
        print(f"{name} и {new_friend_name} садятся на скамейку у озера и разговаривают о жизни и мечтах.")
        print("Вы чувствуете, что между вами возникает романтическое напряжение.")
        print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation("парк", 1)
            quests.append("Встретиться с {new_friend_name} в парке")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, "парк")
        else:
            print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
            manage_skills.chapter_2(gender, name, new_friend_name, "парк")

    # Пример функции для свидания в кино
    def movie_date(gender, name, new_friend_name):
        print("\nВы идете в кино и смотрите фильм вместе.")
        print(f"{name} и {new_friend_name} обсуждают фильм после просмотра и делятся впечатлениями.")
        print("Вы чувствуете, что между вами возникает романтическое напряжение.")
        print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation("кино", 1)
            quests.append("Встретиться с {new_friend_name} в кино")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, "кино")
        else:
            print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
            manage_skills.chapter_2(gender, name, new_friend_name, "кино")

    # Пример функции для свидания на концерте
    def concert_date(gender, name, new_friend_name):
        print("\nВы идете на концерт и наслаждаетесь музыкой вместе.")
        print(f"{name} и {new_friend_name} танцуют и поют, забывая обо всем вокруг.")
        print("Вы чувствуете, что между вами возникает романтическое напряжение.")
        print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation("концерт", 1)
            quests.append("Встретиться с {new_friend_name} на концерте")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, "концерт")
        else:
            print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
            manage_skills.chapter_2(gender, name, new_friend_name, "концерт")

    # Пример функции для свидания в уединенном месте
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
                manage_relationships.update_relationship(new_friend_name, 3)  # Улучшение отношений
            elif choice == "3":
                print(f"Вы обсудили свои чувства и желания с {new_friend_name}. Это укрепило ваши отношения.")
                manage_relationships.update_relationship(new_friend_name, 2)
        else:
            print(f"Вы просто наслаждаетесь обществом {new_friend_name}. Это был приятный вечер.")

        print(f"{new_friend_name}: {name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            print(f"Вы: Я тоже, {new_friend_name}. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_reputation.update_relationship(new_friend_name, 2)
            manage_reputation.update_location_reputation("уединенное место", 1)
            quests.append("Встретиться с {new_friend_name} в уединенном месте")
            manage_skills.check_skills_for_chapter_2(gender, name, new_friend_name, "уединенное место")
        else:
            print(f"Вы: Спасибо за вечер, {new_friend_name}. Но, возможно, это был не самый удачный момент.")
            manage_skills.chapter_2(gender, name, new_friend_name, "уединенное место")

    # Пример функции для выбора специализации
    def choose_specialization(skill):
        print(f"Выберите специализацию для навыка '{skill}':")
        for i, spec in enumerate(specializations[skill], 1):
            print(f"{i}. {spec}")

        choice = input("Введите номер выбора: ")
        if choice.isdigit() and 0 < int(choice) <= len(specializations[skill]):
            return specializations[skill][int(choice) - 1]
        else:
            print("Пожалуйста, введите корректный номер.")
            return choose_specialization(skill)

    # Пример функции для выбора побочного квеста
    def complete_side_quest(quest):
        print(f"Вы выполняете квест: {quest}")
        if quest == "Помочь старушке донести сумки":
            print("Вы помогли старушке и получили в награду домашнее печенье.")
            manage_skills.upgrade_skill("коммуникабельность")
        elif quest == "Найти потерявшегося котенка":
            print("Вы нашли котенка и вернули его хозяину. Котенок был очень рад!")
            manage_skills.upgrade_skill("интеллект")
        elif quest == "Починить сломанный фонтан в парке":
            print("Вы починили фонтан и жители парка благодарят вас за это.")
            manage_skills.upgrade_skill("физическая сила")

        print("Квест выполнен!")
        manage_events.wait(2)
        main_menu(gender, name)
