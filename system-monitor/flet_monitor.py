import psutil
import GPUtil
from tabulate import tabulate
import flet as ft
import threading

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
    disk = psutil.disk_usage('/')
    return {
        'Всего 💿': f'{disk.total / (1024 ** 3):.2f} ГБ',
        'Используется 📂': f'{disk.used / (1024 ** 3):.2f} ГБ',
        'Свободно 🗄️': f'{disk.free / (1024 ** 3):.2f} ГБ',
        'Процент использования 📉': f'{disk.percent}%'
    }

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

def get_top_processes(n=10):
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

def main(page: ft.Page):
    page.title = "Мониторинг системы 🖥️"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.theme_mode = "light"
    page.scroll = ft.ScrollMode.AUTO

    cpu_text = ft.Text(style="headlineSmall", color=ft.colors.BLUE_GREY)
    memory_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)
    disk_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)
    disk_io_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)
    network_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)
    gpu_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)
    processes_text = ft.Text(style="bodyMedium", color=ft.colors.BLUE_GREY)

    def update_metrics():
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
            disk_text.value = "\n".join([f"{key}: {value}" for key, value in disk_usage.items()])
            disk_io_text.value = "\n".join([f"{key}: {value}" for key, value in disk_io.items()])
            network_text.value = "\n".join([f"{key}: {value}" for key, value in network_usage.items()])
            gpu_text.value = tabulate(gpu_usage, headers=['ID', 'Название', 'Загрузка', 'Использование памяти', 'Температура']) if gpu_usage else "GPU не обнаружен или недоступен. 🚫"
            processes_text.value = tabulate(top_processes, headers=['PID', 'Название', 'CPU %', 'Память %'])

            page.update()
            threading.Event().wait(1)  # Обновление каждую секунду

    metrics_list = ft.ListView(
        expand=True,
        controls=[
            ft.Text("Мониторинг системы", style="headlineMedium", color=ft.colors.DEEP_PURPLE),
            ft.Divider(height=10, color="transparent"),
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
        ],
        spacing=10,
        padding=20,
        auto_scroll=True
    )

    page.add(metrics_list)

    # Запуск обновления метрик в отдельном потоке
    threading.Thread(target=update_metrics, daemon=True).start()

ft.app(target=main)
