# Управление квестами

def manage_quests():
    global quests
    # Пример функции для добавления квеста
    def add_quest(quest):
        quests.append(quest)

    # Пример функции для выполнения квеста
    def complete_quest(quest):
        print(f"Вы выполняете квест: {quest}")
        # Добавьте логику выполнения квеста здесь
        print("Квест выполнен!")
        manage_events.wait(2)
        main_menu(gender, name)

    # Пример функции для проверки квестов
    def check_quests():
        if "Встретиться с Алексом в парке" in quests:
            print("Вы можете встретиться с Алексом в парке.")
            # Добавьте логику проверки квеста здесь
            return True
        else:
            return False
