import customtkinter as ctk
import time
import random

# Глобальные переменные
skills = {"коммуникабельность": 0, "интеллект": 0, "физическая сила": 0}
reputation = 0
quests = []

class LoveInTheBigCityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Love in the Big City")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.gender = None
        self.name = None

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Добро пожаловать в текстовую новеллу 'Love in the Big City'!", font=("Arial", 18))
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Начать игру", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        self.label.configure(text="Выберите пол вашего персонажа:")
        self.start_button.pack_forget()

        self.gender_frame = ctk.CTkFrame(self)
        self.gender_frame.pack(pady=20)

        self.male_button = ctk.CTkButton(self.gender_frame, text="Мужчина", command=lambda: self.choose_gender("мужчина"))
        self.male_button.pack(side="left", padx=10)

        self.female_button = ctk.CTkButton(self.gender_frame, text="Женщина", command=lambda: self.choose_gender("женщина"))
        self.female_button.pack(side="left", padx=10)

    def choose_gender(self, gender):
        self.gender = gender
        self.gender_frame.pack_forget()

        self.label.configure(text="Введите имя вашего персонажа:")

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=20)

        self.name_button = ctk.CTkButton(self, text="Продолжить", command=self.set_name)
        self.name_button.pack(pady=20)

    def set_name(self):
        self.name = self.name_entry.get()
        self.name_entry.pack_forget()
        self.name_button.pack_forget()

        self.label.configure(text=f"Вы выбрали играть за {self.gender} по имени {self.name}. Нажмите Enter, чтобы начать...")
        self.start_button.configure(text="Начать", command=self.chapter_1)
        self.start_button.pack(pady=20)

    def chapter_1(self):
        self.label.configure(text=f"{self.name}, вы стоите перед своим новым домом. Куда вы пойдете первым делом?")
        self.start_button.pack_forget()

        self.location_frame = ctk.CTkFrame(self)
        self.location_frame.pack(pady=20)

        self.park_button = ctk.CTkButton(self.location_frame, text="В парк", command=lambda: self.go_to_location("парк"))
        self.park_button.pack(side="left", padx=10)

        self.cafe_button = ctk.CTkButton(self.location_frame, text="В кафе", command=lambda: self.go_to_location("кафе"))
        self.cafe_button.pack(side="left", padx=10)

        self.library_button = ctk.CTkButton(self.location_frame, text="В библиотеку", command=lambda: self.go_to_location("библиотека"))
        self.library_button.pack(side="left", padx=10)

        self.gym_button = ctk.CTkButton(self.location_frame, text="В спортивный зал", command=lambda: self.go_to_location("спортивный зал"))
        self.gym_button.pack(side="left", padx=10)

        self.museum_button = ctk.CTkButton(self.location_frame, text="В музей", command=lambda: self.go_to_location("музей"))
        self.museum_button.pack(side="left", padx=10)

    def go_to_location(self, location):
        self.location_frame.pack_forget()
        if location == "парк":
            self.park()
        elif location == "кафе":
            self.cafe()
        elif location == "библиотека":
            self.library()
        elif location == "спортивный зал":
            self.gym()
        elif location == "музей":
            self.museum()

    def park(self):
        self.label.configure(text=f"Вы пришли в парк и увидели красивую скамейку у озера.\n{self.name}, вы садитесь и наслаждаетесь видом.\nВдруг к вам подходит незнакомец и начинает разговор.")
        self.new_friend_name = "Алекс"
        self.show_dialog(f"Незнакомец: Привет! Я тоже новенький в городе. Меня зовут Алекс. А тебя?", self.park_choice)

    def park_choice(self):
        self.label.configure(text=f"Вы: Привет, Алекс! Меня зовут {self.name}. Приятно познакомиться!\nАлекс: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
        self.show_choice(self.park_decision)

    def park_decision(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы обменялись контактами с Алексом и договорились встретиться снова.")
            skills["коммуникабельность"] += 1
            quests.append("Встретиться с Алексом в парке")
            self.chapter_2("парк")
        else:
            self.label.configure(text="Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            self.chapter_1()

    def cafe(self):
        self.label.configure(text=f"Вы приходите в уютное кафе и заказываете кофе.\n{self.name}, пока вы ждете заказ, к вам подходит официант и предлагает попробовать новый десерт.")
        self.new_friend_name = "Лиза"
        self.show_dialog(f"Официант: Привет! Я вижу, ты новенький. Хочешь попробовать наш новый десерт?", self.cafe_choice)
    
    def cafe_choice(self):
        self.label.configure(text=f"Вы пробуете десерт и он оказывается восхитительным. Официант рад вашей реакции.\nОфициант: Рад, что тебе понравилось! Меня зовут Лиза. А тебя?")
        self.show_dialog(f"Вы: Привет, Лиза! Меня зовут {self.name}. Приятно познакомиться!\nЛиза: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?", self.cafe_decision)

    def cafe_decision(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            skills["коммуникабельность"] += 1
            quests.append("Встретиться с Лизой в кафе")
            self.chapter_2("кафе")
        else:
            self.label.configure(text="Вы вежливо отказались и ушли. Возможно, это было не ваше место.")
            self.chapter_1()

    def library(self):
        self.label.configure(text=f"Вы приходите в библиотеку и начинаете искать интересную книгу.\n{self.name}, вдруг к вам подходит библиотекарь и предлагает помощь.")
        self.new_friend_name = "Макс"
        self.show_dialog(f"Библиотекарь: Привет! Я вижу, ты новенький. Могу помочь найти интересную книгу?", self.library_choice)

    def library_choice(self):
        self.label.configure(text=f"Библиотекарь помогает вам найти отличную книгу.\nБиблиотекарь: Надеюсь, тебе понравится! Меня зовут Макс. А тебя?")
        self.show_dialog(f"Вы: Привет, Макс! Меня зовут {self.name}. Приятно познакомиться!\nМакс: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?", self.library_decision)

    def library_decision(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            skills["интеллект"] += 1
            quests.append("Встретиться с Максом в библиотеке")
            self.chapter_2("библиотека")
        else:
            self.label.configure(text="Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            self.chapter_1()

    def gym(self):
        self.label.configure(text=f"Вы приходите в спортивный зал и начинаете тренировку.\n{self.name}, вдруг к вам подходит тренер и предлагает помощь.")
        self.new_friend_name = "Ник"
        self.show_dialog(f"Тренер: Привет! Я вижу, ты новенький. Хочешь, помогу с тренировкой?", self.gym_choice)

    def gym_choice(self):
        self.label.configure(text=f"Тренер помогает вам с тренировкой и дает полезные советы.\nТренер: Отличная работа! Меня зовут Ник. А тебя?")
        self.show_dialog(f"Вы: Привет, Ник! Меня зовут {self.name}. Приятно познакомиться!\nНик: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?", self.gym_decision)

    def gym_decision(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            skills["физическая сила"] += 1
            quests.append("Встретиться с Ником в спортивном зале")
            self.chapter_2("спортивный зал")
        else:
            self.label.configure(text="Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            self.chapter_1()

    def museum(self):
        self.label.configure(text=f"Вы приходите в музей и начинаете осматривать экспонаты.\n{self.name}, вдруг к вам подходит гид и предлагает экскурсию.")
        self.new_friend_name = "Анна"
        self.show_dialog(f"Гид: Привет! Я вижу, ты новенький. Хочешь, проведу экскурсию?", self.museum_choice)

    def museum_choice(self):
        self.label.configure(text=f"Гид проводит для вас увлекательную экскурсию.\nГид: Надеюсь, тебе понравилось! Меня зовут Анна. А тебя?")
        self.show_dialog(f"Вы: Привет, Анна! Меня зовут {self.name}. Приятно познакомиться!\nАнна: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?", self.museum_decision)

    def museum_decision(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы обменялись контактами с Анной и договорились встретиться снова.")
            skills["интеллект"] += 1
            quests.append("Встретиться с Анной в музее")
            self.chapter_2("музей")
        else:
            self.label.configure(text="Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            self.chapter_1()

    def chapter_2(self, location):
        self.label.configure(text=f"Вы продолжаете встречаться с новым знакомым из {location} и узнаете его/ее лучше.\nВы чувствуете, что между вами возникает что-то особенное.")
        self.show_dialog(f"{self.new_friend_name}: {self.name}, я хотел(а) бы узнать тебя лучше. Может, проведем вместе выходные?", self.chapter_2_choice)

    def chapter_2_choice(self, choice):
        if choice == "да":
            self.label.configure(text=f"Вы соглашаетесь и проводите выходные с {self.new_friend_name}. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
            skills["коммуникабельность"] += 1
            reputation += 1
            self.chapter_3()
        else:
            self.label.configure(text=f"Вы вежливо отказываетесь, но {self.new_friend_name} не сдается и предлагает встретиться позже.")
            self.chapter_2()

    def chapter_3(self):
        self.label.configure(text=f"Вы нашли свою любовь и построили счастливую жизнь в большом городе.\nВы решаете сделать следующий шаг в ваших отношениях.")
        self.show_dialog(f"{self.name}, вы делаете предложение и {self.new_friend_name} соглашается.\nВы начинаете планировать свадьбу и счастливую жизнь вместе.", self.the_end)

    def the_end(self):
        self.label.configure(text=f"Вы, {self.name}, нашли свою любовь и построили счастливую жизнь в большом городе с {self.new_friend_name}.\nСпасибо за игру!")
        self.start_button.configure(text="Выйти", command=self.quit)
        self.start_button.pack(pady=20)

    def show_dialog(self, text, callback):
        self.label.configure(text=text)
        self.choice_frame = ctk.CTkFrame(self)
        self.choice_frame.pack(pady=20)

        self.yes_button = ctk.CTkButton(self.choice_frame, text="Да", command=lambda: callback("да"))
        self.yes_button.pack(side="left", padx=10)

        self.no_button = ctk.CTkButton(self.choice_frame, text="Нет", command=lambda: callback("нет"))
        self.no_button.pack(side="left", padx=10)

    def show_choice(self, callback):
        self.choice_frame = ctk.CTkFrame(self)
        self.choice_frame.pack(pady=20)

        self.yes_button = ctk.CTkButton(self.choice_frame, text="Да", command=lambda: callback("да"))
        self.yes_button.pack(side="left", padx=10)

        self.no_button = ctk.CTkButton(self.choice_frame, text="Нет", command=lambda: callback("нет"))
        self.no_button.pack(side="left", padx=10)

if __name__ == "__main__":
    app = LoveInTheBigCityApp()
    app.mainloop()
