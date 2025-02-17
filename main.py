import customtkinter as ctk
import sqlite3
from sqlite3 import Error
from datetime import datetime
from typing import List, Tuple

# Создание базы данных и таблицы для задач
def create_connection() -> sqlite3.Connection:
    try:
        return sqlite3.connect("todo.db", detect_types=sqlite3.PARSE_DECLTYPES)
    except Error as e:
        print(e)
        raise

def create_table(conn: sqlite3.Connection) -> None:
    try:
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id INTEGER PRIMARY KEY,
                                        task TEXT NOT NULL,
                                        priority TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        deadline TEXT,
                                        completed BOOLEAN NOT NULL
                                    );"""
        with conn:
            conn.execute(sql_create_tasks_table)
    except Error as e:
        print(e)

# Добавление задачи в базу данных
def add_task(conn: sqlite3.Connection, task: str, priority: str, category: str, deadline: datetime.date) -> None:
    sql = '''INSERT INTO tasks(task, priority, category, deadline, completed) VALUES(?, ?, ?, ?, ?)'''
    with conn:
        conn.execute(sql, (task, priority, category, deadline.strftime("%Y-%m-%d"), False))

# Получение всех задач из базы данных
def get_tasks(conn: sqlite3.Connection) -> List[Tuple]:
    with conn:
        cursor = conn.execute("SELECT id, task, priority, category, deadline, completed FROM tasks")
        rows = cursor.fetchall()
        # Преобразуем строки дат в объекты datetime.date
        return [(row[0], row[1], row[2], row[3], datetime.strptime(row[4], "%Y-%m-%d").date() if row[4] else None, row[5]) for row in rows]

# Удаление задачи из базы данных
def delete_task(conn: sqlite3.Connection, task_id: int) -> None:
    sql = 'DELETE FROM tasks WHERE id=?'
    with conn:
        conn.execute(sql, (task_id,))

# Обновление задачи в базе данных
def update_task(conn: sqlite3.Connection, task_id: int, task: str, priority: str, category: str, deadline: datetime.date, completed: bool) -> None:
    sql = '''UPDATE tasks SET task=?, priority=?, category=?, deadline=?, completed=? WHERE id=?'''
    with conn:
        conn.execute(sql, (task, priority, category, deadline.strftime("%Y-%m-%d"), completed, task_id))

# Интерфейс приложения
class TodoApp:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("Список дел")

        ctk.set_appearance_mode("System")  # Меняет тему по умолчанию
        ctk.set_default_color_theme("blue")  # Устанавливает цветовую тему

        self.conn = create_connection()
        if self.conn is not None:
            create_table(self.conn)

        self.task_entry = ctk.CTkEntry(root, width=300, placeholder_text="Введите задачу")
        self.task_entry.pack(pady=10)

        self.priority_entry = ctk.CTkEntry(root, width=300, placeholder_text="Приоритет (Высокий/Средний/Низкий)")
        self.priority_entry.pack(pady=5)

        self.category_entry = ctk.CTkEntry(root, width=300, placeholder_text="Категория")
        self.category_entry.pack(pady=5)

        self.deadline_entry = ctk.CTkEntry(root, width=300, placeholder_text="Дедлайн (дд.мм.гггг)")
        self.deadline_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(root, text="Добавить задачу", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = ctk.CTkTextbox(root, width=300, height=200)
        self.task_listbox.pack(pady=10)

        self.edit_button = ctk.CTkButton(root, text="Редактировать задачу", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.toggle_complete_button = ctk.CTkButton(root, text="Отметить как выполненное", command=self.toggle_complete)
        self.toggle_complete_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(root, text="Удалить задачу", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.theme_switch = ctk.CTkSwitch(root, text="Тёмная тема", command=self.change_theme)
        self.theme_switch.pack(pady=5)

        self.settings_button = ctk.CTkButton(root, text="Настройки", command=self.open_settings)
        self.settings_button.pack(pady=5)

        self.load_tasks()

    def add_task(self) -> None:
        task = self.task_entry.get()
        priority = self.priority_entry.get()
        category = self.category_entry.get()
        deadline_str = self.deadline_entry.get()
        if task and priority and category and deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%d.%m.%Y").date()
                add_task(self.conn, task, priority, category, deadline)
                self.clear_entries()
                self.load_tasks()
            except ValueError:
                self.show_error("Неверный формат даты. Используйте дд.мм.гггг.")

    def load_tasks(self) -> None:
        self.task_listbox.delete("1.0", ctk.END)
        tasks = get_tasks(self.conn)
        for task in tasks:
            status = "Выполнено" if task[5] else "Не выполнено"
            deadline_str = task[4].strftime("%d.%m.%Y") if task[4] else "Нет"
            self.task_listbox.insert(ctk.END, f"{task[0]}. {task[1]} (Приоритет: {task[2]}, Категория: {task[3]}, Дедлайн: {deadline_str}, Статус: {status})\n")

    def delete_task(self) -> None:
        selected_task_id = self.get_selected_task_id()
        if selected_task_id:
            delete_task(self.conn, selected_task_id)
            self.load_tasks()

    def edit_task(self) -> None:
        selected_task_id = self.get_selected_task_id()
        if selected_task_id:
            task = self.task_entry.get()
            priority = self.priority_entry.get()
            category = self.category_entry.get()
            deadline_str = self.deadline_entry.get()
            if task and priority and category and deadline_str:
                try:
                    deadline = datetime.strptime(deadline_str, "%d.%m.%Y").date()
                    completed = self.is_task_completed(selected_task_id)
                    update_task(self.conn, selected_task_id, task, priority, category, deadline, completed)
                    self.load_tasks()
                except ValueError:
                    self.show_error("Неверный формат даты. Используйте дд.мм.гггг.")

    def toggle_complete(self) -> None:
        selected_task_id = self.get_selected_task_id()
        if selected_task_id:
            completed = not self.is_task_completed(selected_task_id)
            task, priority, category, deadline = self.get_task_details(selected_task_id)
            update_task(self.conn, selected_task_id, task, priority, category, deadline, completed)
            self.load_tasks()

    def get_selected_task_id(self) -> int:
        try:
            selected_task = self.task_listbox.get("sel.first", "sel.last")
            task_id = int(selected_task.split(". ")[0])
            return task_id
        except:
            return None

    def is_task_completed(self, task_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute("SELECT completed FROM tasks WHERE id=?", (task_id,))
            result = cursor.fetchone()
        return result[0] if result else False

    def get_task_details(self, task_id: int) -> Tuple[str, str, str, datetime.date]:
        with self.conn:
            cursor = self.conn.execute("SELECT task, priority, category, deadline FROM tasks WHERE id=?", (task_id,))
            result = cursor.fetchone()
        return result if result else ("", "", "", None)

    def clear_entries(self) -> None:
        self.task_entry.delete(0, ctk.END)
        self.priority_entry.delete(0, ctk.END)
        self.category_entry.delete(0, ctk.END)
        self.deadline_entry.delete(0, ctk.END)

    def change_theme(self) -> None:
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        self.refresh_theme()

    def refresh_theme(self) -> None:
        # Обновление интерфейса после смены темы
        self.root.update_idletasks()

    def show_error(self, message: str) -> None:
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Ошибка")
        error_window.geometry("300x100")
        error_label = ctk.CTkLabel(error_window, text=message)
        error_label.pack(pady=20)
        close_button = ctk.CTkButton(error_window, text="Закрыть", command=error_window.destroy)
        close_button.pack(pady=5)

    def open_settings(self) -> None:
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("400x300")

        settings_label = ctk.CTkLabel(settings_window, text="Настройки приложения")
        settings_label.pack(pady=10)

        color_theme_label = ctk.CTkLabel(settings_window, text="Цветовая тема:")
        color_theme_label.pack(pady=5)

        self.theme_var = ctk.StringVar(value="blue")
        color_theme_menu = ctk.CTkOptionMenu(settings_window, values=["blue", "green", "dark-blue"],
                                              command=self.change_color_theme, variable=self.theme_var)
        color_theme_menu.pack(pady=5)

        close_button = ctk.CTkButton(settings_window, text="Закрыть", command=settings_window.destroy)
        close_button.pack(pady=20)

    def change_color_theme(self, new_theme: str) -> None:
        ctk.set_default_color_theme(new_theme)
        self.refresh_theme()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()
