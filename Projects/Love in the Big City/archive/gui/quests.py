quests = []

def manage_quests():
    print("\nВаши квесты:")
    for quest in quests:
        print(f"- {quest}")

def complete_side_quest(quest):
    print(f"\nВы выполняете квест: {quest}")
    if quest == "Помочь старушке донести сумки":
        print("Вы помогли старушке и получили в награду домашнее печенье.")
        upgrade_skill("коммуникабельность")
    elif quest == "Найти потерявшегося котенка":
        print("Вы нашли котенка и вернули его хозяину. Котенок был очень рад!")
        upgrade_skill("интеллект")
    elif quest == "Починить сломанный фонтан в парке":
        print("Вы починили фонтан и жители парка благодарят вас за это.")
        upgrade_skill("физическая сила")
    print("Квест выполнен!")
