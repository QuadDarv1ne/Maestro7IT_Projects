import psutil
import GPUtil
from tabulate import tabulate
import flet as ft
import asyncio

def get_cpu_usage():
    """Получает текущий процент использования CPU."""
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """Получает текущие статистики использования памяти."""
    memory = psutil.virtual_memory()
    return {
        'Всего 💾': f'{memory.total / (1024 ** 3):.2f} ГБ',
        'Используется 🔒': f'{memory.used / (1024 ** 3):.2f} ГБ',
        'Свободно 🔓': f'{memory.available / (1024 ** 3):.2f} ГБ',
        'Процент использования 📊': f'{memory.percent}%'
    }

def get_disk_usage():
    """Получает статистику использования диска для всех разделов."""
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
    """Получает статистику ввода-вывода диска."""
    disk_io = psutil.disk_io_counters()
    return {
        'Чтение (байт) 📄': disk_io.read_bytes,
        'Запись (байт) 💾': disk_io.write_bytes,
        'Чтение (количество) 🔍': disk_io.read_count,
        'Запись (количество) 🖋️': disk_io.write_count
    }

def get_network_usage():
    """Получает статистику использования сети."""
    net_io = psutil.net_io_counters()
    return {
        'Отправлено (байт) 📤': net_io.bytes_sent,
        'Получено (байт) 📥': net_io.bytes_recv,
        'Пакеты отправлены 📦': net_io.packets_sent,
        'Пакеты получены 📫': net_io.packets_recv
    }

def get_gpu_usage():
    """Получает статистику использования GPU."""
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
    """Получает топ процессов по использованию CPU."""
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

async def main(page: ft.Page):
    """Основная функция для инициализации и запуска приложения Flet."""
    page.title = "Мониторинг системы 🖥️"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    cpu_text = ft.Text(style="headlineSmall", color=ft.Colors.BLUE_GREY)
    memory_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)
    disk_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)
    disk_io_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)
    network_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)
    gpu_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)
    processes_text = ft.Text(style="bodyMedium", color=ft.Colors.BLUE_GREY)

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
        bgcolor=ft.Colors.WHITE,
    )

    async def update_metrics():
        """Обновляет системные метрики в интерфейсе Flet."""
        while True:
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()
            disk_usage = get_disk_usage()
            disk_io = get_disk_io()
            network_usage = get_network_usage()
            gpu_usage = get_gpu_usage()
            top_processes = get_top_processes()

            cpu_text.value = f"Загрузка CPU 💻: {cpu_usage}%"
            memory_text.value = "\n".join([f"{key}: {value}" for key, value in memory_usage.items()])
            disk_text.value = tabulate(disk_usage, headers=['Устройство', 'Всего 💿', 'Используется 📂', 'Свободно 🗄️', 'Процент использования 📉'])
            disk_io_text.value = "\n".join([f"{key}: {value}" for key, value in disk_io.items()])
            network_text.value = "\n".join([f"{key}: {value}" for key, value in network_usage.items()])
            gpu_text.value = tabulate(gpu_usage, headers=['ID', 'Название', 'Загрузка', 'Использование памяти', 'Температура']) if gpu_usage else "GPU не обнаружен или недоступен. 🚫"
            processes_text.value = tabulate(top_processes, headers=['PID', 'Название', 'CPU %', 'Память %'])

            page.update()
            await asyncio.sleep(1)  # Обновление каждую секунду

    def change_theme(e, page):
        """Изменяет тему приложения Flet."""
        selected_theme = e.control.value
        theme_map = {
            "Светлая": "light",
            "Темная": "dark",
            "Оранжевая": ft.Theme(color_scheme_seed=ft.Colors.ORANGE),
            "Фиолетовая": ft.Theme(color_scheme_seed=ft.Colors.PURPLE),
            "Синяя": ft.Theme(color_scheme_seed=ft.Colors.BLUE)
        }
        theme = theme_map.get(selected_theme, "light")
        if isinstance(theme, str):
            page.theme_mode = theme
        else:
            page.theme = theme
        page.update()

    async def refresh_metrics(e):
        await update_metrics()

    refresh_button = ft.FloatingActionButton(
        icon=ft.Icons.REFRESH,
        on_click=refresh_metrics,
        bgcolor=ft.Colors.BLUE
    )

    controls = [
        ft.Text("Мониторинг системы", style="headlineMedium", color=ft.Colors.DEEP_PURPLE),
        ft.Divider(height=10, color="purple"),
        ft.Row(
            controls=[
                ft.Column([cpu_text, memory_text], col=6),
                ft.Column([disk_text, disk_io_text], col=6)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        ft.Divider(height=10, color="transparent"),
        network_text,
        ft.Divider(height=10, color="transparent"),
        gpu_text,
        ft.Divider(height=10, color="transparent"),
        processes_text,
        ft.Divider(height=10, color="transparent"),
    ]

    buttons_container = ft.Container(
        content=ft.Row(
            [theme_dropdown, refresh_button],
            alignment=ft.MainAxisAlignment.END
        ),
        alignment=ft.alignment.bottom_right,
        expand=False,
        margin=ft.padding.all(10),
        padding=ft.padding.all(10),
        bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),  # Исправлено использование with_opacity
        border_radius=10,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),  # Исправлено использование with_opacity
            offset=ft.Offset(0, 2)
        ),
    )

    page.overlay.append(buttons_container)
    page.add(ft.ListView(expand=True, controls=controls, spacing=10, padding=20, auto_scroll=True))

    asyncio.create_task(update_metrics())

ft.app(target=main)
