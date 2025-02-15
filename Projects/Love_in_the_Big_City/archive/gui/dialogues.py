relationships = {
    "Алекс": 0,
    "Лиза": 0,
    "Макс": 0,
    "Ник": 0,
    "Анна": 0
}

location_reputation = {
    "парк": 0,
    "кафе": 0,
    "библиотека": 0,
    "спортивный зал": 0,
    "музей": 0
}

adult_content_enabled = False

def update_relationship(name, points):
    if name in relationships:
        relationships[name] += points
        print(f"Ваши отношения с {name} изменились. Текущий уровень: {relationships[name]}")

def update_location_reputation(location, points):
    if location in location_reputation:
        location_reputation[location] += points
        print(f"Ваша репутация в {location} изменилась. Текущий уровень: {location_reputation[location]}")

def toggle_adult_content():
    global adult_content_enabled
    adult_content_enabled = not adult_content_enabled
    status = "включен" if adult_content_enabled else "выключен"
    print(f"Контент 18+ {status}.")
