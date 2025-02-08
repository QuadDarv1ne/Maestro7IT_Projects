import psutil
import GPUtil
from tabulate import tabulate
import argparse

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

def log_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(data + '\n')

def main(top_n, log_file):
    print("=== Мониторинг системы 🖥️ ===")

    cpu_usage = get_cpu_usage()
    print(f"\nЗагрузка CPU 💻: {cpu_usage}%")

    print("\nИспользование памяти:")
    memory_usage = get_memory_usage()
    for key, value in memory_usage.items():
        print(f"{key}: {value}")

    print("\nИспользование диска:")
    disk_usage = get_disk_usage()
    for key, value in disk_usage.items():
        print(f"{key}: {value}")

    print("\nОперации с диском:")
    disk_io = get_disk_io()
    for key, value in disk_io.items():
        print(f"{key}: {value}")

    print("\nИспользование сети:")
    network_usage = get_network_usage()
    for key, value in network_usage.items():
        print(f"{key}: {value}")

    print("\nИспользование GPU:")
    gpu_usage = get_gpu_usage()
    if gpu_usage:
        print(tabulate(gpu_usage,
                       headers=['ID', 'Название', 'Загрузка', 'Использование памяти', 'Температура'],
                       tablefmt='grid'))
    else:
        print("GPU не обнаружен или недоступен. 🚫")

    print("\nТоп процессов по использованию CPU 🏆:")
    top_processes = get_top_processes(top_n)
    print(tabulate(top_processes,
                   headers=['PID', 'Название', 'CPU %', 'Память %'],
                   tablefmt='grid'))

    if log_file:
        log_data = (f"CPU Usage: {cpu_usage}%\n"
                    f"Memory Usage: {memory_usage}\n"
                    f"Disk Usage: {disk_usage}\n"
                    f"Disk IO: {disk_io}\n"
                    f"Network Usage: {network_usage}\n"
                    f"GPU Usage:\n{tabulate(gpu_usage, headers=['ID', 'Name', 'Load', 'Memory Usage', 'Temperature'], tablefmt='plain')}\n"
                    f"Top Processes:\n{tabulate(top_processes, headers=['PID', 'Name', 'CPU %', 'Memory %'], tablefmt='plain')}\n")
        log_to_file(log_file, log_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Мониторинг системы.')
    parser.add_argument('--top', type=int, default=10, help='Количество топ-процессов для отображения')
    parser.add_argument('--log', type=str, default=None, help='Файл для записи логов')
    args = parser.parse_args()

    main(args.top, args.log)
