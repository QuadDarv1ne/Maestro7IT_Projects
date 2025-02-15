import json
from pathlib import Path

class Location:
    def __init__(self, data):
        self.name = data["name"]
        self.type = data["type"]
        self.reputation = data["initial_reputation"]
        self.max_reputation = data["max_reputation"]
        self.activities = data["activities"]
        self.popular_characters = data["popular_characters"]

    def update_reputation(self, points):
        self.reputation = max(0, min(self.max_reputation, self.reputation + points))

    def __repr__(self):
        return f"Location(name={self.name}, reputation={self.reputation})"

class LocationManager:
    def __init__(self):
        self.locations = self.load_locations()

    def load_locations(self):
        locations_data = self.load_json_data("data/locations")
        return {loc["name"]: Location(loc) for loc in locations_data}

    def load_json_data(self, directory):
        data = []
        for file_path in Path(directory).glob("*.json"):
            with open(file_path, "r", encoding="utf-8") as file:
                data.append(json.load(file))
        return data

    def get_location(self, name):
        return self.locations.get(name)

    def update_location_reputation(self, name, points):
        location = self.get_location(name)
        if location:
            location.update_reputation(points)
            print(f"Репутация локации {name} обновлена до {location.reputation}")
        else:
            print(f"Локация {name} не найдена.")

# Пример использования
# if __name__ == "__main__":
#     manager = LocationManager()
#     manager.update_location_reputation("парк", 10)
#     manager.update_location_reputation("кафе", 5)
#     print(manager.locations)
