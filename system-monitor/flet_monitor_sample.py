import psutil
import GPUtil
from tabulate import tabulate
import flet as ft
import threading
import time
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Функции для получения метрик
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        'Всего 💾': f'{memory.total / (1024 ** 3):.2f} ГБ',
        'Используется 🔒': f'{memory.used / (1024 ** 3):.2f} ГБ',
        'Свободно 🔓': f'{memory.available / (1024 ** 3):.2f} ГБ',
        'Процент использования 📊': f'{memory.percent}%'
    }

def get_disk_usage():
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append([
                partition.device,
                f'{usage.total / (1024 ** 3):.2f} ГБ',
                f'{usage.used / (1024 ** 3):.2f} ГБ',
                f'{usage.free / (1024 ** 3):.2f} ГБ',
                f'{usage.percent}%'
            ])
        except PermissionError:
            continue
    return disk_info

def get_disk_io():
    disk_io = psutil.disk_io_counters()
    return {
        'Чтение (байт) 📄': disk_io.read_bytes,
        'Запись (байт) 💾': disk_io.write_bytes,
        'Чтение (количество) 🔍': disk_io.read_count,
        'Запись (количество) 🖋️': disk_io.write_count
    }

def get_network_usage():
    net_io = psutil.net_io_counters()
    return {
        'Отправлено (байт) 📤': net_io.bytes_sent,
        'Получено (байт) 📥': net_io.bytes_recv,
        'Пакеты отправлены 📦': net_io.packets_sent,
        'Пакеты получены 📫': net_io.packets_recv
    }

def get_gpu_usage():
    try:
        gpus = GPUtil.getGPUs()
        gpu_list = []
        for gpu in gpus:
            gpu_list.append([
                gpu.id,
                gpu.name,
                f"{gpu.load * 100:.2f}%",
                f"{gpu.memoryUtil * 100:.2f}%",
                f"{gpu.temperature} °C 🌡️"
            ])
        return gpu_list
    except Exception as e:
        print(f"Ошибка при получении информации о GPU: {e}")
        return []

def get_top_processes(n=20):
    processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                       key=lambda x: x.info['cpu_percent'],
                       reverse=True)[:n]:
        try:
            processes.append([
                proc.info['pid'],
                proc.info['name'],
                f"{proc.info['cpu_percent']:.2f}%",
                f"{proc.info['memory_percent']:.2f}%"
            ])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

# Функция для создания графиков
def plot_metrics(cpu_data, memory_data):
    plt.switch_backend('Agg')  # Use a non-GUI backend
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # График использования CPU
    ax[0].plot(cpu_data, label="CPU Usage %", color="blue")
    ax[0].set_title("CPU Usage Over Time")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Usage (%)")
    ax[0].legend()

    # График использования памяти
    ax[1].plot(memory_data, label="Memory Usage %", color="orange")
    ax[1].set_title("Memory Usage Over Time")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Usage (%)")
    ax[1].legend()

    plt.tight_layout()

    # Сохраняем график в буфер
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Основная функция для инициализации и запуска приложения Flet
def main(page: ft.Page):
    page.title = "Мониторинг системы 🖥️"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Создание карточек для метрик
    cpu_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Загрузка CPU 💻", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    memory_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Использование памяти 💾", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    disk_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Использование диска 💿", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    disk_io_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Диск I/O 📄", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    network_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Сеть 🌐", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    gpu_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("GPU 🎮", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    processes_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Топ процессов 🔝", style="headlineSmall"),
                    ft.Text("", style="bodyMedium", color=ft.colors.BLUE_GREY)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    graph_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Графики 📈", style="headlineSmall"),
                    ft.Image(src="", width=600, height=400)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
            padding=10
        )
    )

    theme_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Светлая"),
            ft.dropdown.Option("Темная"),
            ft.dropdown.Option("Оранжевая"),
            ft.dropdown.Option("Фиолетовая"),
            ft.dropdown.Option("Синяя")
        ],
        on_change=lambda e: change_theme(e, page),
        width=150,
        bgcolor=ft.colors.WHITE,
    )

    def update_metrics():
        try:
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()
            disk_usage = get_disk_usage()
            disk_io = get_disk_io()
            network_usage = get_network_usage()
            gpu_usage = get_gpu_usage()
            top_processes = get_top_processes()

            cpu_card.content.content.controls[1].value = f"Загрузка CPU 💻: {cpu_usage}%"
            memory_card.content.content.controls[1].value = "\n".join([f"{key}: {value}" for key, value in memory_usage.items()])
            disk_card.content.content.controls[1].value = tabulate(disk_usage, headers=['Устройство', 'Всего 💿', 'Используется 📂', 'Свободно 🗄️', 'Процент использования 📉'], tablefmt="fancy_grid")
            disk_io_card.content.content.controls[1].value = "\n".join([f"{key}: {value}" for key, value in disk_io.items()])
            network_card.content.content.controls[1].value = "\n".join([f"{key}: {value}" for key, value in network_usage.items()])
            gpu_card.content.content.controls[1].value = tabulate(gpu_usage, headers=['ID', 'Название', 'Загрузка', 'Использование памяти', 'Температура'], tablefmt="fancy_grid") if gpu_usage else "GPU не обнаружен или недоступен. 🚫"
            processes_card.content.content.controls[1].value = tabulate(top_processes, headers=['PID', 'Название', 'CPU %', 'Память %'], tablefmt="fancy_grid")

            page.update()
        except Exception as e:
            print(f"Ошибка при обновлении метрик: {e}")

    def change_theme(e, page):
        selected_theme = e.control.value
        theme_map = {
            "Светлая": "light",
            "Темная": "dark",
            "Оранжевая": ft.Theme(color_scheme_seed=ft.colors.ORANGE),
            "Фиолетовая": ft.Theme(color_scheme_seed=ft.colors.PURPLE),
            "Синяя": ft.Theme(color_scheme_seed=ft.colors.BLUE)
        }
        theme = theme_map.get(selected_theme, "light")
        if isinstance(theme, str):
            page.theme_mode = theme
        else:
            page.theme = theme
        page.update()

    def refresh_metrics(e):
        update_metrics()

    refresh_button = ft.FloatingActionButton(
        icon=ft.icons.REFRESH,
        on_click=refresh_metrics,
        bgcolor=ft.colors.BLUE
    )

    # Создание вкладок для различных метрик
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="CPU", content=cpu_card),
            ft.Tab(text="Память", content=memory_card),
            ft.Tab(text="Диски", content=disk_card),
            ft.Tab(text="Диск I/O", content=disk_io_card),
            ft.Tab(text="Сеть", content=network_card),
            ft.Tab(text="GPU", content=gpu_card),
            ft.Tab(text="Процессы", content=processes_card),
            ft.Tab(text="Графики", content=graph_card)
        ],
        expand=1
    )

    # Создание контейнера для кнопок
    buttons_container = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Row(
                    [theme_dropdown, refresh_button],
                    alignment=ft.MainAxisAlignment.END
                ),
                alignment=ft.alignment.bottom_right,
                padding=ft.padding.only(right=20, bottom=20)
            )
        ],
        width=page.width,
        height=page.height
    )

    # Добавление контейнера с кнопками на страницу
    page.controls.append(tabs)
    page.controls.append(buttons_container)

    # Обновление метрик каждую секунду
    def update_metrics_periodically():
        cpu_data = []
        memory_data = []
        while True:
            try:
                cpu_data.append(get_cpu_usage())
                memory_data.append(float(get_memory_usage()['Процент использования 📊'].replace('%', '')))
                if len(cpu_data) > 60:  # Ограничиваем количество точек данных
                    cpu_data.pop(0)
                    memory_data.pop(0)

                buf = plot_metrics(cpu_data, memory_data)
                graph_card.content.content.controls[1].src_base64 = base64.b64encode(buf.getvalue()).decode()
                buf.close()

                update_metrics()
                time.sleep(1)
            except Exception as e:
                print(f"Ошибка при периодическом обновлении метрик: {e}")

    threading.Thread(target=update_metrics_periodically, daemon=True).start()

ft.app(target=main)
