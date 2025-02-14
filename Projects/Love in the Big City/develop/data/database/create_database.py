import sqlite3
import json
import os

def create_database(db_path='love_in_the_big_city.db'):
    """
    Создает базу данных и таблицы, если они не существуют.
    """
    # Получаем путь к директории базы данных
    db_dir = os.path.dirname(db_path)

    # Проверяем, существует ли директория, если нет - создаем
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            print(f"Директория {db_dir} успешно создана.")
        except OSError as e:
            print(f"Ошибка при создании директории {db_dir}: {e}")
            return

    # Проверка существования базы данных и создание новой базы данных
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Создание таблицы персонажей, если она не существует
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

            # Создание таблицы локаций, если она не существует
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
            print(f"База данных {db_path} создана или уже существует.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
        return

def populate_characters_and_locations(db_path='love_in_the_big_city.db'):
    """
    Заполняет таблицы персонажей и локаций данными.
    """

    # Данные о персонажах
    characters_data = [
        {"name": "Александр", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["дружелюбный", "спортивный", "амбициозный"], "description": "Дружелюбный парень, любит спорт и активный отдых.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "парк"},
        {"name": "Лиза", "gender": "female", "orientation": "bi", "romanceable": True, "traits": ["весёлая", "творческая", "открытая"], "description": "Официантка в кафе, добрая и отзывчивая.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "кафе"},
        {"name": "Максим", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["интеллектуальный", "спокойный", "натурал"], "description": "Библиотекарь-интеллектуал, ценит тишину и книги.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "библиотека"},
        {"name": "Николай", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["энергичный", "дружелюбный", "творческий"], "description": "Тренер в спортивном зале, уверенный в себе.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "спортивный зал"},
        {"name": "Анна", "gender": "female", "orientation": "straight", "romanceable": True, "traits": ["умная", "заботливая", "романтичная"], "description": "Гид в музее, увлечена историей.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "музей"},
        {"name": "Катя", "gender": "female", "orientation": "lesbian", "romanceable": True, "traits": ["весёлая", "авантюрная", "открытая"], "description": "Веселая девушка с пляжа, любит приключения.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "пляж"},
        {"name": "Вика", "gender": "female", "orientation": "bi", "romanceable": True, "traits": ["креативная", "энергичная", "независимая"], "description": "Диджей в ночном клубе, свободолюбивая и яркая.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "ночной клуб"},
        {"name": "Настя", "gender": "female", "orientation": "straight", "romanceable": True, "traits": ["дружелюбная", "романтичная", "мечтательная"], "description": "Работница парка аттракционов, мечтательная и романтичная.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "парк аттракционов"},
        {"name": "Надежда", "gender": "female", "orientation": "straight", "romanceable": False, "traits": ["мудрая", "заботливая", "добрая"], "description": "Учительница, добрая и мудрая.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "библиотека"},
        {"name": "Любовь", "gender": "female", "orientation": "straight", "romanceable": False, "traits": ["романтичная", "мечтательная", "добрая"], "description": "Владелица цветочного магазина, романтичная натура.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "парк"},
        {"name": "Вероника", "gender": "female", "orientation": "lesbian", "romanceable": True, "traits": ["творческая", "загадочная", "интеллектуальная"], "description": "Художница, увлеченная своим творчеством.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "музей"},
        {"name": "Вера", "gender": "female", "orientation": "straight", "romanceable": False, "traits": ["заботливая", "добрая", "ответственная"], "description": "Медсестра, заботливая и ответственная.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "кафе"},
        {"name": "Мария", "gender": "female", "orientation": "straight", "romanceable": False, "traits": ["умная", "амбициозная", "дружелюбная"], "description": "Журналистка, всегда в поиске интересных историй.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "библиотека"},
        {"name": "Иван", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["общительный", "дружелюбный", "ответственный"], "description": "Бармен в ночном клубе, общительный и дружелюбный.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "ночной клуб"},
        {"name": "Дмитрий", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["ответственный", "внимательный", "организованный"], "description": "Администратор в парке аттракционов, ответственный и внимательный.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "парк аттракционов"},
        {"name": "Сергей", "gender": "male", "orientation": "straight", "romanceable": True, "traits": ["интеллектуальный", "философский", "спокойный"], "description": "Владелец книжного магазина, любит литературу и философию.", "initial_relationship": 0, "max_relationship": 100, "favorite_location": "библиотека"}
    ]

    # Данные о локациях
    locations_data = [
        {"name": "парк", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["прогулки", "пикники", "игры"], "popular_characters": ["Александр", "Катя", "Николай"]},
        {"name": "кафе", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["поесть", "поговорить"], "popular_characters": ["Лиза", "Анна"]},
        {"name": "библиотека", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["читать", "учиться"], "popular_characters": ["Максим", "Надежда", "Мария", "Сергей"]},
        {"name": "спортивный зал", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["тренировки", "занятия спортом"], "popular_characters": ["Николай", "Иван"]},
        {"name": "музей", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["экскурсии", "посещение выставок"], "popular_characters": ["Анна", "Вероника"]},
        {"name": "пляж", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["загорать", "плавание"], "popular_characters": ["Катя"]},
        {"name": "ночной клуб", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["танцы", "встречи"], "popular_characters": ["Вика", "Иван"]},
        {"name": "парк аттракционов", "type": "public", "initial_reputation": 0, "max_reputation": 100, "activities": ["катания", "развлечения"], "popular_characters": ["Настя", "Дмитрий"]}
    ]

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Вставка данных о персонажах
            for character in characters_data:
                cursor.execute('''
                INSERT OR REPLACE INTO characters (name, gender, orientation, romanceable, traits, description, initial_relationship, max_relationship, favorite_location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (character['name'], character['gender'], character['orientation'], character['romanceable'],
                      json.dumps(character['traits']), character['description'], character['initial_relationship'],
                      character['max_relationship'], character['favorite_location']))

            # Вставка данных о локациях
            for location in locations_data:
                cursor.execute('''
                INSERT OR REPLACE INTO locations (name, type, initial_reputation, max_reputation, activities, popular_characters)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (location['name'], location['type'], location['initial_reputation'], location['max_reputation'],
                      json.dumps(location['activities']), json.dumps(location['popular_characters'])))

            conn.commit()
            print(f"Данные успешно добавлены в базу данных {db_path}.")
    
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")

if __name__ == "__main__":
    db_path = 'C:/temp/love_in_the_big_city.db'  # Убедитесь, что это доступный путь
    create_database(db_path)
    populate_characters_and_locations(db_path)
