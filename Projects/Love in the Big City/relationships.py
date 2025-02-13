# Управление отношениями

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

def manage_relationships():
    global relationships, location_reputation

    # Пример функции для улучшения отношений
    def update_relationship(name, points):
        if name in relationships:
            relationships[name] += points
            print(f"Ваши отношения с {name} изменились. Текущий уровень: {relationships[name]}")

            # Уникальные бонусы за высокий уровень отношений
            if relationships[name] >= 10:
                print(f"Вы достигли высокого уровня отношений с {name} и получили уникальный бонус!")
                manage_skills.upgrade_skill("харизма")

    # Пример функции для улучшения репутации в локации
    def update_location_reputation(location, points):
        if location in location_reputation:
            location_reputation[location] += points
            print(f"Ваша репутация в {location} изменилась. Текущий уровень: {location_reputation[location]}")
