import psutil
import GPUtil
from tabulate import tabulate
import flet as ft
import asyncio
import datetime

# Constants for UI
TEXT_COLOR = ft.colors.BLACK
THEME_SEED = ft.colors.BLUE
UPDATE_INTERVAL = 2

async def get_cpu_usage():
    """Retrieves the current CPU usage percentage with error handling."""
    try:
        return await asyncio.to_thread(psutil.cpu_percent, interval=1)
    except Exception as e:
        print(f"Error retrieving CPU usage: {e}")
        return 0

async def get_memory_usage():
    """Retrieves the current memory usage statistics with error handling."""
    try:
        memory = await asyncio.to_thread(psutil.virtual_memory)
        return {
            'Total': f'{memory.total / (1024 ** 3):.2f} GB',
            'Used': f'{memory.used / (1024 ** 3):.2f} GB',
            'Available': f'{memory.available / (1024 ** 3):.2f} GB',
            'Percentage': f'{memory.percent}%'
        }
    except Exception as e:
        print(f"Error retrieving memory usage: {e}")
        return {}

async def get_disk_usage():
    """Retrieves the disk usage statistics for all partitions with error handling."""
    try:
        partitions = await asyncio.to_thread(psutil.disk_partitions)
        disk_info = []
        for partition in partitions:
            try:
                usage = await asyncio.to_thread(psutil.disk_usage, partition.mountpoint)
                disk_info.append([
                    partition.device,
                    f'{usage.total / (1024 ** 3):.2f} GB',
                    f'{usage.used / (1024 ** 3):.2f} GB',
                    f'{usage.free / (1024 ** 3):.2f} GB',
                    f'{usage.percent}%'
                ])
            except PermissionError:
                continue
        return disk_info
    except Exception as e:
        print(f"Error retrieving disk usage: {e}")
        return []

async def get_disk_io():
    """Retrieves the disk I/O statistics with error handling."""
    try:
        disk_io = await asyncio.to_thread(psutil.disk_io_counters)
        return {
            'Read (bytes)': disk_io.read_bytes,
            'Write (bytes)': disk_io.write_bytes,
            'Read count': disk_io.read_count,
            'Write count': disk_io.write_count
        }
    except Exception as e:
        print(f"Error retrieving disk I/O: {e}")
        return {}

async def get_network_usage():
    """Retrieves the network usage statistics with error handling."""
    try:
        net_io = await asyncio.to_thread(psutil.net_io_counters)
        return {
            'Sent (bytes)': net_io.bytes_sent,
            'Received (bytes)': net_io.bytes_recv,
            'Packets sent': net_io.packets_sent,
            'Packets received': net_io.packets_recv
        }
    except Exception as e:
        print(f"Error retrieving network usage: {e}")
        return {}

async def get_gpu_usage():
    """Retrieves the GPU usage statistics with error handling."""
    try:
        gpus = await asyncio.to_thread(GPUtil.getGPUs)
        gpu_list = []
        for gpu in gpus:
            gpu_list.append([
                gpu.id,
                gpu.name,
                f"{gpu.load * 100:.2f}%",
                f"{gpu.memoryUtil * 100:.2f}%",
                f"{gpu.temperature} °C"
            ])
        return gpu_list
    except Exception as e:
        print(f"Error retrieving GPU info: {e}")
        return []

async def get_top_processes(n=20):
    """Retrieves the top processes by CPU usage with error handling."""
    try:
        processes = []
        for proc in sorted(await asyncio.to_thread(psutil.process_iter, ['pid', 'name', 'cpu_percent', 'memory_percent']),
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
    except Exception as e:
        print(f"Error retrieving top processes: {e}")
        return []

def save_logs(cpu_usage, memory_usage, disk_usage, disk_io, network_usage, gpu_usage, top_processes):
    """Saves the system monitoring logs to a file with error handling."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"system_log_{timestamp}.txt"

        with open(filename, 'w') as file:
            file.write(f"CPU Usage: {cpu_usage}%\n")
            file.write("Memory Usage:\n")
            for key, value in memory_usage.items():
                file.write(f"{key}: {value}\n")
            file.write("Disk Usage:\n")
            file.write(tabulate(disk_usage, headers=['Device', 'Total', 'Used', 'Free', 'Percentage']))
            file.write("\nDisk IO:\n")
            for key, value in disk_io.items():
                file.write(f"{key}: {value}\n")
            file.write("\nNetwork Usage:\n")
            for key, value in network_usage.items():
                file.write(f"{key}: {value}\n")
            file.write("\nGPU Usage:\n")
            if gpu_usage:
                file.write(tabulate(gpu_usage, headers=['ID', 'Name', 'Load', 'Memory Util', 'Temperature']))
            else:
                file.write("GPU not detected or unavailable.")
            file.write("\nTop Processes:\n")
            file.write(tabulate(top_processes, headers=['PID', 'Name', 'CPU %', 'Memory %']))

        print(f"Logs saved to {filename}")
    except Exception as e:
        print(f"Error saving logs: {e}")

async def update_metrics(page, cpu_text, memory_text, disk_text, disk_io_text, network_text, gpu_text, processes_text):
    """Updates the system metrics in the Flet interface."""
    while True:
        cpu_usage = await get_cpu_usage()
        memory_usage = await get_memory_usage()
        disk_usage = await get_disk_usage()
        disk_io = await get_disk_io()
        network_usage = await get_network_usage()
        gpu_usage = await get_gpu_usage()
        top_processes = await get_top_processes()

        cpu_text.value = f"CPU Usage: {cpu_usage}%"
        memory_text.value = "\n".join([f"{key}: {value}" for key, value in memory_usage.items()])
        disk_text.value = tabulate(disk_usage, headers=['Device', 'Total', 'Used', 'Free', 'Percentage'])
        disk_io_text.value = "\n".join([f"{key}: {value}" for key, value in disk_io.items()])
        network_text.value = "\n".join([f"{key}: {value}" for key, value in network_usage.items()])
        gpu_text.value = tabulate(gpu_usage, headers=['ID', 'Name', 'Load', 'Memory Util', 'Temperature']) if gpu_usage else "GPU not detected or unavailable."
        processes_text.value = tabulate(top_processes, headers=['PID', 'Name', 'CPU %', 'Memory %'])

        page.update()
        await asyncio.sleep(UPDATE_INTERVAL)  # Update every UPDATE_INTERVAL seconds

async def main(page: ft.Page):
    """Initializes and runs the Flet application."""
    page.title = "System Monitoring 🖥️"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed=THEME_SEED)

    # Text elements for displaying metrics
    cpu_text = ft.Text(style="headlineSmall", color=TEXT_COLOR)
    memory_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)
    disk_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)
    disk_io_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)
    network_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)
    gpu_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)
    processes_text = ft.Text(style="bodyMedium", color=TEXT_COLOR)

    async def refresh_metrics(e):
        await update_metrics(page, cpu_text, memory_text, disk_text, disk_io_text, network_text, gpu_text, processes_text)

    refresh_button = ft.FloatingActionButton(
        icon=ft.icons.REFRESH,
        on_click=refresh_metrics,
        bgcolor=ft.colors.BLUE,
        tooltip="Refresh metrics"
    )

    async def save_logs_handler(e):
        cpu_usage = await get_cpu_usage()
        memory_usage = await get_memory_usage()
        disk_usage = await get_disk_usage()
        disk_io = await get_disk_io()
        network_usage = await get_network_usage()
        gpu_usage = await get_gpu_usage()
        top_processes = await get_top_processes()
        save_logs(cpu_usage, memory_usage, disk_usage, disk_io, network_usage, gpu_usage, top_processes)

    save_button = ft.FloatingActionButton(
        icon=ft.icons.SAVE,
        on_click=save_logs_handler,
        bgcolor=ft.colors.GREEN,
        tooltip="Save logs"
    )

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="CPU & Memory", content=ft.Column([cpu_text, memory_text])),
            ft.Tab(text="Disk", content=ft.Column([disk_text, disk_io_text])),
            ft.Tab(text="Network", content=network_text),
            ft.Tab(text="GPU", content=gpu_text),
            ft.Tab(text="Processes", content=processes_text),
        ],
        expand=True,
    )

    scrollable_listview = ft.ListView(
        expand=True,
        controls=[
            ft.Text("System Monitoring", style="headlineMedium", color=ft.colors.BLUE),
            ft.Divider(height=10, color=ft.colors.PURPLE),
            tabs
        ],
        spacing=10,
        padding=20,
        auto_scroll=True
    )

    buttons_container = ft.Container(
        content=ft.Row(
            [refresh_button, save_button],
            alignment=ft.MainAxisAlignment.END
        ),
        alignment=ft.Alignment(1, 1),
        margin=ft.margin.all(10),
        padding=ft.padding.all(10),
        border_radius=10
    )

    page.overlay.append(buttons_container)
    page.add(scrollable_listview)

    asyncio.create_task(update_metrics(page, cpu_text, memory_text, disk_text, disk_io_text, network_text, gpu_text, processes_text))

ft.app(target=main)

"""
    Заметки по коду ...
    1. Решить проблемы с цветопередачей
    2. 
    3. 
"""
