import json
from pathlib import Path

class Character:
    def __init__(self, data):
        self.name = data["name"]
        self.gender = data["gender"]
        self.orientation = data["orientation"]
        self.romanceable = data["romanceable"]
        self.traits = data["traits"]
        self.relationship = data["initial_relationship"]
        self.max_relationship = data["max_relationship"]
        self.favorite_location = data["favorite_location"]

    def update_relationship(self, points):
        self.relationship = max(0, min(self.max_relationship, self.relationship + points))

    def __repr__(self):
        return f"Character(name={self.name}, relationship={self.relationship})"

class CharacterManager:
    def __init__(self):
        self.characters = self.load_characters()

    def load_characters(self):
        characters_data = self.load_json_data("data/characters/males") + self.load_json_data("data/characters/females")
        return {char["name"]: Character(char) for char in characters_data}

    def load_json_data(self, directory):
        data = []
        for file_path in Path(directory).glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                data.append(json.load(file))
        return data

    def get_character(self, name):
        return self.characters.get(name)

    def update_character_relationship(self, name, points):
        character = self.get_character(name)
        if character:
            character.update_relationship(points)
            print(f"Отношения с {name} обновлены до {character.relationship}")
        else:
            print(f"Персонаж {name} не найден.")

# Пример использования
# if __name__ == "__main__":
#     manager = CharacterManager()
#     manager.update_character_relationship("Александр", 10)
#     manager.update_character_relationship("Лиза", 5)
#     print(manager.characters)
