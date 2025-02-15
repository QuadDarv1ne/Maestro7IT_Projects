import json

def save_game(gender, name, slot=1):
    game_state = {
        "name": name,
        "gender": gender,
        "skills": skills,
        "reputation": reputation,
        "location_reputation": location_reputation,
        "relationships": relationships,
        "quests": quests,
        "achievements": achievements_list,
        "current_chapter": "Глава 1"
    }
    with open(f"save_game_slot_{slot}.json", "w") as file:
        json.dump(game_state, file)
    print(f"Игра сохранена в слот {slot}!")

def load_game(slot=1):
    try:
        with open(f"save_game_slot_{slot}.json", "r") as file:
            game_state = json.load(file)
            global name, gender, skills, reputation, location_reputation, relationships, quests, achievements_list
            name = game_state["name"]
            gender = game_state["gender"]
            skills = game_state["skills"]
            reputation = game_state["reputation"]
            location_reputation = game_state["location_reputation"]
            relationships = game_state["relationships"]
            quests = game_state["quests"]
            achievements_list = game_state["achievements"]
            print(f"Игра загружена из слота {slot}!")
            main_menu(gender, name)
    except FileNotFoundError:
        print(f"Сохранение в слоте {slot} не найдено. Начните новую игру.")
        start_game()
