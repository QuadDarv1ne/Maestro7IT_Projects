import pygame
import customtkinter as ctk
import json
import random
import time

# Initialize Pygame mixer
pygame.mixer.init()

# Load the music file
music_file = "music/Korandrino - HappyTropical.mp3"
pygame.mixer.music.load(music_file)

# Global variables
skills = {
    "коммуникабельность": 0,
    "интеллект": 0,
    "физическая сила": 0,
    "харизма": 0,
    "удача": 0
}

reputation = 0
quests = []
achievements_list = []
inventory = []

skill_tree = {
    "коммуникабельность": {"level": 0, "specialization": None},
    "интеллект": {"level": 0, "specialization": None},
    "физическая сила": {"level": 0, "specialization": None},
    "харизма": {"level": 0, "specialization": None},
    "удача": {"level": 0, "specialization": None}
}

specializations = {
    "коммуникабельность": ["оратор", "переговорщик"],
    "интеллект": ["аналитик", "исследователь"],
    "физическая сила": ["боец", "спортсмен"],
    "харизма": ["лидер", "общительный"],
    "удача": ["игрок", "авантюрист"]
}

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

current_time = "день"
current_weather = "ясно"

class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Любовь в большом городе :D")
        self.geometry("800x600")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.text_box = ctk.CTkTextbox(self.main_frame, wrap="word", height=300)
        self.text_box.pack(pady=10, padx=10, fill="both", expand=True)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=10, fill="x")

        self.buttons = []
        for i in range(4):
            button = ctk.CTkButton(self.button_frame, text=f"Option {i+1}", command=lambda i=i: self.button_click(i))
            button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            self.buttons.append(button)

        self.volume_slider = ctk.CTkSlider(self.main_frame, from_=0, to=1, orientation="horizontal", command=self.adjust_volume)
        self.volume_slider.pack(pady=10, padx=10, fill="x")
        self.volume_slider.set(0.05)  # Set default volume to 5%

        self.enable_adult_content()
        self.play_music()

    def play_music(self):
        # Play the music indefinitely
        pygame.mixer.music.play(loops=-1)

    def display_text(self, text):
        self.text_box.insert(ctk.END, text + "\n")
        self.text_box.see(ctk.END)

    def set_button_texts(self, texts):
        for i, button in enumerate(self.buttons):
            if i < len(texts):
                button.configure(text=texts[i])
                button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            else:
                button.pack_forget()

    def button_click(self, index):
        if self.current_function:
            self.current_function(index)

    def enable_adult_content(self):
        self.display_text("\nВнимание! Эта игра содержит контент 18+.")
        self.display_text("Пожалуйста, подтвердите, что вам есть 18 лет.")
        self.set_button_texts(["Да, мне есть 18 лет", "Нет, мне нет 18 лет"])
        self.current_function = self.confirm_adult_content

    def confirm_adult_content(self, choice):
        if choice == 0:
            global adult_content_enabled
            adult_content_enabled = True
            self.display_text("Контент 18+ включен. Продолжайте игру.")
            self.start_game()
        else:
            self.display_text("Контент 18+ отключен. Вы можете продолжить игру без этого контента.")
            self.start_game()

    def start_game(self):
        self.display_text("Добро пожаловать в текстовую новеллу 'Love in the Big City :D'")
        self.display_text("Вы - молодой человек/девушка, который/ая только что переехал/а в большой город.")
        self.display_text("Ваша цель - найти свою любовь и построить счастливую жизнь.")
        self.choose_gender()

    def choose_gender(self):
        self.display_text("\nВыберите пол вашего персонажа:")
        self.set_button_texts(["Мужчина", "Женщина"])
        self.current_function = self.set_gender

    def set_gender(self, choice):
        self.gender = "мужчина" if choice == 0 else "женщина"
        self.display_text(f"\nВы выбрали играть за {self.gender}.")
        self.enter_name()

    def enter_name(self):
        self.display_text("\nВведите имя вашего персонажа:")
        self.name_entry = ctk.CTkEntry(self.main_frame)
        self.name_entry.pack(pady=10, padx=10, fill="x")
        self.name_entry.bind("<Return>", self.set_name)

    def set_name(self, event):
        self.name = self.name_entry.get()
        self.display_text(f"\nВы выбрали имя {self.name}.")
        self.name_entry.destroy()
        self.chapter_1()

    def chapter_1(self):
        self.display_text("\nГлава 1: Новый дом")
        self.display_text(f"{self.name}, вы стоите перед своим новым домом. Куда вы пойдете первым делом?")
        self.set_button_texts(["В парк", "В кафе", "В библиотеку", "В спортивный зал", "В музей", "На прогулку по городу"])
        self.current_function = self.handle_chapter_1_choice

    def handle_chapter_1_choice(self, choice):
        if choice == 0:
            self.park()
        elif choice == 1:
            self.cafe()
        elif choice == 2:
            self.library()
        elif choice == 3:
            self.gym()
        elif choice == 4:
            self.museum()
        elif choice == 5:
            self.city_walk()
        else:
            self.display_text("Пожалуйста, введите корректный номер.")
            self.chapter_1()

    def park(self):
        self.display_text("\nВы пришли в парк и увидели красивую скамейку у озера.")
        self.display_text(f"{self.name}, вы садитесь и наслаждаетесь видом.")
        self.display_text("Вдруг к вам подходит незнакомец и начинает разговор.")
        self.set_button_texts([
            f"Привет, Алекс! Меня зовут {self.name}. Приятно познакомиться!",
            "Здравствуйте! Я Алекс, недавно переехал сюда. А как тебя зовут?",
            "Хэй! Я Алекс, новенький в этих краях. А ты кто?"
        ])
        self.current_function = self.handle_park_choice

    def handle_park_choice(self, choice):
        self.display_text("Алекс: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_park_decision

    def handle_park_decision(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Алексом и договорились встретиться снова.")
            skills["коммуникабельность"] += 1
            update_relationship("Алекс", 2)
            update_location_reputation("парк", 1)
            quests.append("Встретиться с Алексом в парке")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Алекс", -1)
            update_location_reputation("парк", -1)
            self.chapter_1()

    def cafe(self):
        self.display_text("\nВы приходите в уютное кафе и заказываете кофе.")
        self.display_text(f"{self.name}, пока вы ждете заказ, к вам подходит официант и предлагает попробовать новый десерт.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_cafe_choice

    def handle_cafe_choice(self, choice):
        if choice == 0:
            self.display_text("Вы пробуете десерт и он оказывается восхитительным. Официант рад вашей реакции.")
            self.display_text("Официант: Рад, что тебе понравилось! Меня зовут Лиза. А тебя?")
            self.set_button_texts([f"Привет, Лиза! Меня зовут {self.name}. Приятно познакомиться!"])
            self.current_function = self.handle_cafe_decision
        else:
            self.display_text("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
            self.chapter_1()

    def handle_cafe_decision(self, choice):
        if choice == 0:
            self.display_text(f"Лиза: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
            self.set_button_texts(["Да", "Нет"])
            self.current_function = self.handle_cafe_final_choice
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Лиза", -1)
            update_location_reputation("кафе", -1)
            self.chapter_1()

    def handle_cafe_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Лизой и договорились встретиться снова.")
            skills["коммуникабельность"] += 1
            update_relationship("Лиза", 2)
            update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это было не ваше место.")
            update_relationship("Лиза", -1)
            update_location_reputation("кафе", -1)
            self.chapter_1()

    def library(self):
        self.display_text("\nВы приходите в библиотеку и начинаете искать интересную книгу.")
        self.display_text(f"{self.name}, вдруг к вам подходит библиотекарь и предлагает помощь.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_library_choice

    def handle_library_choice(self, choice):
        if choice == 0:
            self.display_text("Библиотекарь помогает вам найти отличную книгу.")
            self.display_text("Библиотекарь: Надеюсь, тебе понравится! Меня зовут Макс. А тебя?")
            self.set_button_texts([f"Привет, Макс! Меня зовут {self.name}. Приятно познакомиться!"])
            self.current_function = self.handle_library_decision
        else:
            self.display_text("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это было не ваше место.")
            self.chapter_1()

    def handle_library_decision(self, choice):
        if choice == 0:
            self.display_text(f"Макс: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
            self.set_button_texts(["Да", "Нет"])
            self.current_function = self.handle_library_final_choice
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Макс", -1)
            update_location_reputation("библиотека", -1)
            self.chapter_1()

    def handle_library_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Максом и договорились встретиться снова.")
            skills["интеллект"] += 1
            update_relationship("Макс", 2)
            update_location_reputation("библиотека", 1)
            quests.append("Встретиться с Максом в библиотеке")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Макс", -1)
            update_location_reputation("библиотека", -1)
            self.chapter_1()

    def gym(self):
        self.display_text("\nВы приходите в спортивный зал и начинаете тренировку.")
        self.display_text(f"{self.name}, вдруг к вам подходит тренер и предлагает помощь.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_gym_choice

    def handle_gym_choice(self, choice):
        if choice == 0:
            self.display_text("Тренер помогает вам с тренировкой и дает полезные советы.")
            self.display_text("Тренер: Отличная работа! Меня зовут Ник. А тебя?")
            self.set_button_texts([f"Привет, Ник! Меня зовут {self.name}. Приятно познакомиться!"])
            self.current_function = self.handle_gym_decision
        else:
            self.display_text("Вы отказываетесь от помощи и продолжаете тренировку самостоятельно. Возможно, это было не ваше место.")
            self.chapter_1()

    def handle_gym_decision(self, choice):
        if choice == 0:
            self.display_text(f"Ник: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
            self.set_button_texts(["Да", "Нет"])
            self.current_function = self.handle_gym_final_choice
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Ник", -1)
            update_location_reputation("спортивный зал", -1)
            self.chapter_1()

    def handle_gym_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Ником и договорились встретиться снова.")
            skills["физическая сила"] += 1
            update_relationship("Ник", 2)
            update_location_reputation("спортивный зал", 1)
            quests.append("Встретиться с Ником в спортивном зале")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Ник", -1)
            update_location_reputation("спортивный зал", -1)
            self.chapter_1()

    def museum(self):
        self.display_text("\nВы приходите в музей и начинаете осматривать экспонаты.")
        self.display_text(f"{self.name}, вдруг к вам подходит гид и предлагает экскурсию.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_museum_choice

    def handle_museum_choice(self, choice):
        if choice == 0:
            self.display_text("Гид проводит для вас увлекательную экскурсию.")
            self.display_text("Гид: Надеюсь, тебе понравится! Меня зовут Анна. А тебя?")
            self.set_button_texts([f"Привет, Анна! Меня зовут {self.name}. Приятно познакомиться!"])
            self.current_function = self.handle_museum_decision
        else:
            self.display_text("Вы отказываетесь от экскурсии и продолжаете осмотр самостоятельно. Возможно, это было не ваше место.")
            self.chapter_1()

    def handle_museum_decision(self, choice):
        if choice == 0:
            self.display_text(f"Анна: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
            self.set_button_texts(["Да", "Нет"])
            self.current_function = self.handle_museum_final_choice
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Анна", -1)
            update_location_reputation("музей", -1)
            self.chapter_1()

    def handle_museum_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Анной и договорились встретиться снова.")
            skills["интеллект"] += 1
            update_relationship("Анна", 2)
            update_location_reputation("музей", 1)
            quests.append("Встретиться с Анной в музее")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Анна", -1)
            update_location_reputation("музей", -1)
            self.chapter_1()

    def city_walk(self):
        self.display_text("\nВы решили прогуляться по городу и наслаждаетесь его атмосферой.")
        self.display_text("Вдруг вы замечаете что-то интересное.")
        self.set_button_texts(["Подойти и рассмотреть.", "Продолжить прогулку.", "Сделать фотографию."])
        self.current_function = self.handle_city_walk_choice

    def handle_city_walk_choice(self, choice):
        if choice == 0:
            self.display_text("Вы подошли и увидели старинную вывеску. Это вызвало у вас интерес.")
            skills["интеллект"] += 1
        elif choice == 1:
            self.display_text("Вы продолжили прогулку, наслаждаясь видами города.")
            skills["коммуникабельность"] += 1
        elif choice == 2:
            self.display_text("Вы сделали фотографию. Это будет отличный сувенир!")
            skills["харизма"] += 1

        self.display_text("Прогулка по городу была приятной и полезной.")
        manage_events.wait(2)
        self.main_menu(self.gender, self.name)

    def check_skills_for_chapter_2(self):
        if sum(skills.values()) >= required_skills_for_chapter_2:
            self.chapter_2(self.gender, self.name)
        else:
            self.display_text(f"Вам нужно набрать еще {required_skills_for_chapter_2 - sum(skills.values())} навыков, чтобы перейти к следующей главе.")
            self.chapter_1()

    def chapter_2(self, gender, name):
        self.display_text("\nГлава 2: Новые знакомства")
        self.display_text(f"Вы продолжаете встречаться с новым знакомым и узнаете его/ее лучше.")
        self.display_text(f"Вы чувствуете, что между вами возникает что-то особенное.")
        self.display_text(f"{name}, я провел(а) отличное время с тобой. Спасибо за этот вечер.")

        if adult_content_enabled:
            self.display_text("Вы решаете провести интимное время вместе.")
            self.intimate_scene()
        else:
            self.display_text("Вы решаете продолжить знакомство и узнать друг друга лучше.")
            self.continue_relationship()

    def intimate_scene(self):
        self.display_text("\nИнтимная сцена")
        self.display_text("Вы проводите время вместе, наслаждаясь обществом друг друга.")
        self.display_text("Этот момент укрепляет ваши отношения и добавляет новые эмоции.")
        skills["харизма"] += 1
        global reputation
        reputation += 2
        unlock_achievement("Любовь с первого взгляда")
        self.continue_relationship()

    def continue_relationship(self):
        self.display_text("\nПродолжение отношений")
        self.display_text("Вы продолжаете встречаться и узнаете друг друга лучше.")
        self.display_text("Ваши отношения становятся крепче с каждым днем.")
        self.romantic_date(self.gender, self.name)

    def romantic_date(self, gender, name):
        self.display_text("\nРомантическое свидание")
        self.display_text("Куда вы хотите пойти?")
        self.set_button_texts(["В ресторан", "На прогулку по парку", "В кино", "На концерт", "В уединенное место"])
        self.current_function = self.handle_romantic_date_choice

    def handle_romantic_date_choice(self, choice):
        if choice == 0:
            self.restaurant_date(gender, name)
        elif choice == 1:
            self.park_date(gender, name)
        elif choice == 2:
            self.movie_date(gender, name)
        elif choice == 3:
            self.concert_date(gender, name)
        elif choice == 4:
            self.private_date(gender, name)
        else:
            self.display_text("Пожалуйста, введите корректный номер.")
            self.romantic_date(gender, name)

    def restaurant_date(self, gender, name):
        self.display_text("\nВы приходите в ресторан и заказываете ужин.")
        self.display_text(f"{name}, пока вы ждете заказ, к вам подходит официант и предлагает попробовать новый десерт.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_restaurant_date_choice

    def handle_restaurant_date_choice(self, choice):
        if choice == 0:
            self.display_text("Вы пробуете десерт и он оказывается восхитительным. Официант рад вашей реакции.")
            self.display_text("Официант: Рад, что тебе понравилось! Меня зовут Лиза. А тебя?")
            self.set_button_texts([f"Привет, Лиза! Меня зовут {name}. Приятно познакомиться!"])
            self.current_function = self.handle_restaurant_date_decision
        else:
            self.display_text("Вы просто выпиваете кофе и уходите. Возможно, это было не ваше место.")
            self.chapter_1()

    def handle_restaurant_date_decision(self, choice):
        if choice == 0:
            self.display_text(f"Лиза: Приятно познакомиться, {name}! Может, обменяемся контактами и встретимся снова?")
            self.set_button_texts(["Да", "Нет"])
            self.current_function = self.handle_restaurant_date_final_choice
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Лиза", -1)
            update_location_reputation("кафе", -1)
            self.chapter_1()

    def handle_restaurant_date_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Лизой и договорились встретиться снова.")
            skills["коммуникабельность"] += 1
            update_relationship("Лиза", 2)
            update_location_reputation("кафе", 1)
            quests.append("Встретиться с Лизой в кафе")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            update_relationship("Лиза", -1)
            update_location_reputation("кафе", -1)
            self.chapter_1()

    def park_date(self, gender, name):
        self.display_text("\nВы решили прогуляться по парку с новым знакомым.")
        self.display_text(f"{name}, вы наслаждаетесь природой и беседуете.")
        self.display_text(f"{name}: Это место такое умиротворяющее. Я рад(а), что мы здесь вместе.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            self.display_text(f"Вы соглашаетесь и продолжаете прогулку, наслаждаясь обществом друг друга.")
            skills["коммуникабельность"] += 1
            global reputation
            reputation += 1
            unlock_achievement("Любовь с первого взгляда")
            self.romantic_date(gender, name)
        else:
            self.display_text(f"Вы вежливо отказываетесь, но {name} не сдается и предлагает встретиться позже.")
            self.chapter_2(gender, name)

    def movie_date(self, gender, name):
        self.display_text("\nВы решили сходить в кино с новым знакомым.")
        self.display_text(f"{name}, вы выбираете фильм и наслаждаетесь просмотром.")
        self.display_text(f"{name}: Фильм был отличный! Я рад(а), что мы смотрели его вместе.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            self.display_text(f"Вы соглашаетесь и продолжаете обсуждать фильм, наслаждаясь обществом друг друга.")
            skills["коммуникабельность"] += 1
            global reputation
            reputation += 1
            unlock_achievement("Любовь с первого взгляда")
            self.romantic_date(gender, name)
        else:
            self.display_text(f"Вы вежливо отказываетесь, но {name} не сдается и предлагает встретиться позже.")
            self.chapter_2(gender, name)

    def concert_date(self, gender, name):
        self.display_text("\nВы решили сходить на концерт с новым знакомым.")
        self.display_text(f"{name}, вы наслаждаетесь музыкой и атмосферой.")
        self.display_text(f"{name}: Концерт был потрясающий! Я рад(а), что мы были здесь вместе.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            self.display_text(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая концерт.")
            skills["коммуникабельность"] += 1
            global reputation
            reputation += 1
            unlock_achievement("Любовь с первого взгляда")
            self.romantic_date(gender, name)
        else:
            self.display_text(f"Вы вежливо отказываетесь, но {name} не сдается и предлагает встретиться позже.")
            self.chapter_2(gender, name)

    def private_date(self, gender, name):
        self.display_text("\nВы решили провести время в уединенном месте с новым знакомым.")
        self.display_text(f"{name}, вы наслаждаетесь тишиной и обществом друг друга.")
        self.display_text(f"{name}: Это место такое спокойное. Я рад(а), что мы здесь вместе.")

        choice = input("Введите 'да' или 'нет': ").lower()
        if choice == "да":
            self.display_text(f"Вы соглашаетесь и продолжаете наслаждаться вечером, обсуждая разные темы.")
            skills["коммуникабельность"] += 1
            global reputation
            reputation += 1
            unlock_achievement("Любовь с первого взгляда")
            self.romantic_date(gender, name)
        else:
            self.display_text(f"Вы вежливо отказываетесь, но {name} не сдается и предлагает встретиться позже.")
            self.chapter_2(gender, name)

    def unlock_achievement(achievement_name):
        for achievement in achievements_list:
            if achievement["name"] == achievement_name:
                achievement["unlocked"] = True
                print(f"Достижение разблокировано: {achievement_name}!")
                if achievement["reward"]:
                    print(f"Вы получили награду: {achievement['reward']}")
                    # Здесь можно добавить логику для применения награды
                break

    def main_menu(self, gender, name):
        self.display_text("\nГлавное меню")
        self.set_button_texts(["1. Продолжить игру", "2. Сохранить игру", "3. Загрузить игру", "4. Выйти из игры"])
        self.current_function = self.handle_main_menu_choice

    def handle_main_menu_choice(self, choice):
        if choice == 0:
            self.chapter_1()
        elif choice == 1:
            save_game(gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list)
            print("Игра сохранена!")
            self.main_menu(gender, name)
        elif choice == 2:
            gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list = load_game()
            print("Игра загружена!")
            self.main_menu(gender, name)
        elif choice == 3:
            print("Спасибо за игру! До новых встреч!")
        else:
            print("Пожалуйста, введите корректный номер.")
            self.main_menu(gender, name)

    def save_game(gender, name, skills, reputation, quests, relationships, location_reputation, achievements_list):
        game_data = {
            "gender": gender,
            "name": name,
            "skills": skills,
            "reputation": reputation,
            "quests": quests,
            "relationships": relationships,
            "location_reputation": location_reputation,
            "achievements_list": achievements_list
        }
        with open("save_game.json", "w") as file:
            json.dump(game_data, file)

    def load_game():
        with open("save_game.json", "r") as file:
            game_data = json.load(file)
        return (
            game_data["gender"],
            game_data["name"],
            game_data["skills"],
            game_data["reputation"],
            game_data["quests"],
            game_data["relationships"],
            game_data["location_reputation"],
            game_data["achievements_list"]
        )

    def update_relationship(name, points):
        if name in relationships:
            relationships[name] += points
            print(f"Ваши отношения с {name} изменились. Текущий уровень: {relationships[name]}")

            if relationships[name] >= 15:
                print(f"Ваши отношения с {name} достигли нового уровня. Вы можете провести интимное время вместе.")

    def update_location_reputation(location, points):
        if location in location_reputation:
            location_reputation[location] += points
            print(f"Ваша репутация в {location} изменилась. Текущий уровень: {location_reputation[location]}")

    def manage_skills(skill, points):
        if skill in skills:
            skills[skill] += points
            print(f"Ваш навык '{skill}' улучшен. Текущий уровень: {skills[skill]}")

    def manage_relationships(name, points):
        update_relationship(name, points)

    def manage_quests(quest):
        quests.append(quest)
        print(f"Новый квест добавлен: {quest}")

    def manage_achievements(achievement_name):
        unlock_achievement(achievement_name)

    def manage_events():
        time.sleep(2)

    def manage_dialogues():
        pass

    def play_music(self):
        pygame.mixer.music.play(loops=-1)
        self.adjust_volume(None)  # Set initial volume

    def adjust_volume(self, event):
        volume = self.volume_slider.get()
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
