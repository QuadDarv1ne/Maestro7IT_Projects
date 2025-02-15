import sqlite3
import json
import os

def create_database(db_name='love_in_the_big_city.db'):
    """
    Создает базу данных и таблицы, если они не существуют.
    """
    current_dir = os.getcwd()
    db_path = os.path.join(current_dir, db_name)

    if not os.path.exists(db_path):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    orientation TEXT NOT NULL,
                    romanceable BOOLEAN NOT NULL,
                    traits TEXT NOT NULL,
                    description TEXT NOT NULL,
                    initial_relationship INTEGER NOT NULL,
                    max_relationship INTEGER NOT NULL,
                    favorite_location TEXT NOT NULL
                )
                ''')

                cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    initial_reputation INTEGER NOT NULL,
                    max_reputation INTEGER NOT NULL,
                    activities TEXT NOT NULL,
                    popular_characters TEXT NOT NULL
                )
                ''')

                conn.commit()
                print(f"База данных {db_path} успешно создана.")
        except sqlite3.Error as e:
            print(f"Ошибка при создании базы данных: {e}")
            return
    else:
        print(f"База данных {db_path} уже существует.")


def populate_characters_and_locations(db_name='love_in_the_big_city.db'):
    """
    Заполняет таблицы персонажей и локаций данными.
    """
    current_dir = os.getcwd()

    db_path = os.path.join(current_dir, db_name)

    characters_file_path = os.path.join(current_dir, 'Projects', 'Love_in_the_Big_City', 'develop', 'data', 'characters.json')
    locations_file_path = os.path.join(current_dir, 'Projects', 'Love_in_the_Big_City', 'develop', 'data', 'locations.json')

    try:
        with open(characters_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            characters_data = data.get('characters', [])

        with open(locations_file_path, 'r', encoding='utf-8') as f:
            locations_data = json.load(f)
            # Извлекаем список локаций из словаря
            locations_data = locations_data.get('locations', [])

        if not isinstance(characters_data, list):
            raise ValueError("Данные в файле characters.json должны быть списком!")

        if not isinstance(locations_data, list):
            raise ValueError("Данные в файле locations.json должны быть списком!")

        print(f"Загружено {len(characters_data)} персонажей и {len(locations_data)} локаций.")

    except FileNotFoundError as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
        return
    except ValueError as e:
        print(f"Ошибка в формате данных: {e}")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Вставка данных о персонажах
            for character in characters_data:
                if isinstance(character, dict):  
                    cursor.execute('''
                    INSERT INTO characters (name, gender, orientation, romanceable, traits, description, initial_relationship, max_relationship, favorite_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (character['name'], character['gender'], character['orientation'], character['romanceable'],
                          json.dumps(character['traits']), character['description'], character['initial_relationship'],
                          character['max_relationship'], character['favorite_location']))

            # Вставка данных о локациях
            for location in locations_data:
                if isinstance(location, dict):  
                    cursor.execute('''
                    INSERT INTO locations (name, type, initial_reputation, max_reputation, activities, popular_characters)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (location['name'], location['type'], location['initial_reputation'], location['max_reputation'],
                          json.dumps(location['activities']), json.dumps(location['popular_characters'])))

            conn.commit()
            print(f"Данные успешно добавлены в базу данных {db_path}.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")


if __name__ == "__main__":
    create_database()
    populate_characters_and_locations()
