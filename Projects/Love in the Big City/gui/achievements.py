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
        upgrade_skill("коммуникабельность")
    elif reward == "Бонус к харизме":
        upgrade_skill("харизма")
    elif reward == "Бонус к интеллекту":
        upgrade_skill("интеллект")
    elif reward == "Бонус к физической силе":
        upgrade_skill("физическая сила")
    elif reward == "Бонус к удаче":
        upgrade_skill("удача")
    elif reward == "Бонус к репутации":
        global reputation
        reputation += 1
