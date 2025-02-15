import customtkinter as ctk
from skills import manage_skills
from quests import manage_quests
from achievements import manage_achievements
from events import manage_events
from dialogues import manage_dialogues
from save_load import save_game, load_game

class GameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Любовь в большом городе")
        self.geometry("800x600")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.text_box = ctk.CTkTextbox(self.main_frame, wrap="word", height=300)
        self.text_box.pack(pady=10, padx=10, fill="both", expand=True)

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10, padx=10, fill="x")

        self.buttons = []
        for i in range(4):
            button = ctk.CTkButton(self.button_frame, text=f"Option {i+1}", command=lambda i=i: self.button_click(i))
            button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            self.buttons.append(button)

        self.start_game()

    def start_game(self):
        self.display_text("Добро пожаловать в текстовую новеллу 'Love in the Big City'!")
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
        self.set_button_texts(["В парк", "В кафе", "В библиотеку", "В спортивный зал"])
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

    def park(self):
        self.display_text("\nВы пришли в парк и увидели красивую скамейку у озера.")
        self.display_text(f"{self.name}, вы садитесь и наслаждаетесь видом.")
        self.display_text("Вдруг к вам подходит незнакомец и начинает разговор.")
        self.set_button_texts(["Привет, Алекс! Меня зовут {self.name}. Приятно познакомиться!",
                                "Здравствуйте, Алекс. Я {self.name}. Рад(а) встрече.",
                                "Хэй, Алекс! Я {self.name}. Как тебе город пока?"])
        self.current_function = self.handle_park_choice

    def handle_park_choice(self, choice):
        self.display_text("Алекс: Приятно познакомиться! Может, обменяемся контактами и встретимся снова?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_park_decision

    def handle_park_decision(self, choice):
        if choice == 0:
            self.display_text("Вы обменялись контактами с Алексом и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_dialogues.update_relationship("Алекс", 2)
            manage_dialogues.update_location_reputation("парк", 1)
            manage_quests.append("Встретиться с Алексом в парке")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш человек.")
            manage_dialogues.update_relationship("Алекс", -1)
            manage_dialogues.update_location_reputation("парк", -1)
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
        self.display_text(f"Лиза: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_cafe_final_decision

    def handle_cafe_final_decision(self, choice):
        if choice == 0:
            self.display_text(f"Вы обменялись контактами с Лизой и договорились встретиться снова.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_dialogues.update_relationship("Лиза", 2)
            manage_dialogues.update_location_reputation("кафе", 1)
            manage_quests.append("Встретиться с Лизой в кафе")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это было не ваше место.")
            manage_dialogues.update_relationship("Лиза", -1)
            manage_dialogues.update_location_reputation("кафе", -1)
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
            self.display_text("Вы отказываетесь от помощи и продолжаете поиск самостоятельно. Возможно, это был не ваш день.")
            self.chapter_1()

    def handle_library_decision(self, choice):
        self.display_text(f"Макс: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_library_final_decision

    def handle_library_final_decision(self, choice):
        if choice == 0:
            self.display_text(f"Вы обменялись контактами с Максом и договорились встретиться снова.")
            manage_skills.upgrade_skill("интеллект")
            manage_dialogues.update_relationship("Макс", 2)
            manage_dialogues.update_location_reputation("библиотека", 1)
            manage_quests.append("Встретиться с Максом в библиотеке")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            manage_dialogues.update_relationship("Макс", -1)
            manage_dialogues.update_location_reputation("библиотека", -1)
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
            self.display_text("Вы отказываетесь от помощи и продолжаете тренировку самостоятельно. Возможно, это был не ваш день.")
            self.chapter_1()

    def handle_gym_decision(self, choice):
        self.display_text(f"Ник: Приятно познакомиться, {self.name}! Может, обменяемся контактами и встретимся снова?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_gym_final_decision

    def handle_gym_final_decision(self, choice):
        if choice == 0:
            self.display_text(f"Вы обменялись контактами с Ником и договорились встретиться снова.")
            manage_skills.upgrade_skill("физическая сила")
            manage_dialogues.update_relationship("Ник", 2)
            manage_dialogues.update_location_reputation("спортивный зал", 1)
            manage_quests.append("Встретиться с Ником в спортивном зале")
            self.check_skills_for_chapter_2()
        else:
            self.display_text("Вы вежливо отказались и ушли. Возможно, это был не ваш день.")
            manage_dialogues.update_relationship("Ник", -1)
            manage_dialogues.update_location_reputation("спортивный зал", -1)
            self.chapter_1()

    def check_skills_for_chapter_2(self):
        if sum(manage_skills.skill_tree.values()) >= manage_skills.required_skills_for_chapter_2:
            self.chapter_2()
        else:
            self.display_text(f"Вам нужно набрать еще {manage_skills.required_skills_for_chapter_2 - sum(manage_skills.skill_tree.values())} навыков, чтобы перейти к следующей главе.")
            self.chapter_1()

    def chapter_2(self):
        self.display_text("\nГлава 2: Новые знакомства")
        self.display_text(f"Вы продолжаете встречаться с новым знакомым и узнаете его/ее лучше.")
        self.display_text(f"Вы чувствуете, что между вами возникает что-то особенное.")
        self.display_text(f"Может, проведем вместе выходные?")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_chapter_2_choice

    def handle_chapter_2_choice(self, choice):
        if choice == 0:
            self.display_text("Вы соглашаетесь и проводите выходные вместе. Вы узнаете друг друга лучше и чувствуете, что между вами возникает что-то особенное.")
            manage_skills.upgrade_skill("коммуникабельность")
            manage_achievements.unlock_achievement("Любовь с первого взгляда")
            self.romantic_date()
        else:
            self.display_text("Вы вежливо отказываетесь, но ваш новый знакомый не сдается и предлагает встретиться позже.")
            self.chapter_2()

    def romantic_date(self):
        self.display_text("\nРомантическое свидание")
        self.display_text("Куда вы хотите пойти?")
        self.set_button_texts(["В ресторан", "На прогулку по парку", "В кино", "На концерт"])
        self.current_function = self.handle_romantic_date_choice

    def handle_romantic_date_choice(self, choice):
        if choice == 0:
            self.restaurant_date()
        elif choice == 1:
            self.park_date()
        elif choice == 2:
            self.movie_date()
        elif choice == 3:
            self.concert_date()

    def restaurant_date(self):
        self.display_text("\nВы приходите в ресторан и заказываете ужин.")
        self.display_text("Вдруг официант приносит вам комплимент от шефа - десерт на выбор!")
        self.set_button_texts(["Поблагодарить официанта и насладиться десертом.",
                                "Предложить разделить десерт с вашим спутником.",
                                "Попросить упаковать десерт с собой."])
        self.current_function = self.handle_restaurant_date_choice

    def handle_restaurant_date_choice(self, choice):
        if choice == 0:
            self.display_text("Вы поблагодарили официанта и насладились десертом.")
        elif choice == 1:
            self.display_text("Вы предложили разделить десерт со своим спутником. Это был романтический жест, который укрепил ваши отношения.")
            manage_dialogues.update_relationship("Алекс", 2)
        elif choice == 2:
            self.display_text("Вы попросили упаковать десерт с собой.")

        self.display_text("Ваш спутник: Спасибо за этот вечер.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_restaurant_date_final_choice

    def handle_restaurant_date_final_choice(self, choice):
        if choice == 0:
            self.display_text("Вы: Я тоже. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            self.chapter_3()
        else:
            self.display_text("Вы: Спасибо за вечер. Но, возможно, это был не самый удачный момент.")
            self.chapter_2()

    def park_date(self):
        self.display_text("\nВы гуляете по парку, наслаждаясь природой и обществом друг друга.")
        self.display_text("Вы чувствуете, что между вами возникает романтическое напряжение.")
        self.display_text("Ваш спутник: Спасибо за этот вечер.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_park_date_choice

    def handle_park_date_choice(self, choice):
        if choice == 0:
            self.display_text("Вы: Я тоже. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            self.chapter_3()
        else:
            self.display_text("Вы: Спасибо за вечер. Но, возможно, это был не самый удачный момент.")
            self.chapter_2()

    def movie_date(self):
        self.display_text("\nВы идете в кино и смотрите фильм вместе.")
        self.display_text("Вы обсуждаете фильм после просмотра и делитесь впечатлениями.")
        self.display_text("Вы чувствуете, что между вами возникает романтическое напряжение.")
        self.display_text("Ваш спутник: Спасибо за этот вечер.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_movie_date_choice

    def handle_movie_date_choice(self, choice):
        if choice == 0:
            self.display_text("Вы: Я тоже. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            self.chapter_3()
        else:
            self.display_text("Вы: Спасибо за вечер. Но, возможно, это был не самый удачный момент.")
            self.chapter_2()

    def concert_date(self):
        self.display_text("\nВы идете на концерт и наслаждаетесь музыкой вместе.")
        self.display_text("Вы танцуете и поете, забывая обо всем вокруг.")
        self.display_text("Вы чувствуете, что между вами возникает романтическое напряжение.")
        self.display_text("Ваш спутник: Спасибо за этот вечер.")
        self.set_button_texts(["Да", "Нет"])
        self.current_function = self.handle_concert_date_choice

    def handle_concert_date_choice(self, choice):
        if choice == 0:
            self.display_text("Вы: Я тоже. Давай продолжим наше свидание.")
            manage_skills.upgrade_skill("коммуникабельность")
            self.chapter_3()
        else:
            self.display_text("Вы: Спасибо за вечер. Но, возможно, это был не самый удачный момент.")
            self.chapter_2()

    def chapter_3(self):
        self.display_text("\nГлава 3: Вместе навсегда")
        self.display_text("Вы нашли свою любовь и построили счастливую жизнь в большом городе.")
        self.display_text("Вы решаете сделать следующий шаг в ваших отношениях.")
        self.display_text("Вы делаете предложение и ваш спутник соглашается.")
        self.display_text("Вы начинаете планировать свадьбу и счастливую жизнь вместе.")
        self.the_end()

    def the_end(self):
        self.display_text("\nКонец")
        self.display_text("Вы нашли свою любовь и построили счастливую жизнь в большом городе.")
        self.display_text("Спасибо за игру!")

    def display_text(self, text):
        self.text_box.insert("end", text + "\n")
        self.text_box.see("end")

    def set_button_texts(self, texts):
        for i, button in enumerate(self.buttons):
            if i < len(texts):
                button.configure(text=texts[i])
                button.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            else:
                button.pack_forget()

    def button_click(self, index):
        if hasattr(self, 'current_function'):
            self.current_function(index)
