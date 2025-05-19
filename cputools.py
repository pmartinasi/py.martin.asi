import psutil
import time
import platform

def get_cpu_temp():
    try:
        # Solo disponible en algunos sistemas (Linux con lm-sensors)
        temps = psutil.sensors_temperatures()
        if not temps:
            return "No disponible"
        for name, entries in temps.items():
            for entry in entries:
                if "cpu" in entry.label.lower() or "core" in entry.label.lower():
                    return f"{entry.current}°C"
        return "No disponible"
    except Exception as e:
        return f"Error: {e}"

def get_disk_temp():
    try:
        # Usar smartctl (requiere sudo)
        import subprocess
        output = subprocess.check_output(['sudo', 'smartctl', '-A', '/dev/sda'], text=True)
        for line in output.splitlines():
            if "Temperature" in line or "temp" in line.lower():
                return line
        return "No disponible"
    except Exception as e:
        return f"Error: {e}"

def get_cpu_usage():
    return f"{psutil.cpu_percent(interval=1)}%"

def get_ram_usage():
    mem = psutil.virtual_memory()
    return f"{mem.percent}% usado ({round(mem.used / (1024**3), 2)} GB de {round(mem.total / (1024**3), 2)} GB)"

def get_disk_usage():
    usages = []
    for part in psutil.disk_partitions():
        if part.fstype != "":
            usage = psutil.disk_usage(part.mountpoint)
            usages.append(f"{part.mountpoint}: {usage.percent}% usado ({round(usage.used / (1024**3), 2)} GB de {round(usage.total / (1024**3), 2)} GB)")
    return usages

def mostrar_estado():
    print("=" * 50)
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"CPU Temp: {get_cpu_temp()}")
    print(f"Disco Temp: {get_disk_temp()}")
    print(f"Uso CPU: {get_cpu_usage()}")
    print(f"Uso RAM: {get_ram_usage()}")
    print("Uso Discos:")
    for disk in get_disk_usage():
        print(f"  - {disk}")
    print("=" * 50)

if __name__ == "__main__":
    while True:
        mostrar_estado()
        time.sleep(5)  # Intervalo de actualización en segundos
