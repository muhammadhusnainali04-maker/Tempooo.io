import psutil
import random
import wmi
from plyer import notification
import time

try:
    computer = wmi.WMI()
except Exception:
    computer = None

# Global variable to prevent notification spam
last_alert_time = 0

def get_hardware_names():
    cpu_name = "Unknown CPU"
    gpu_name = "Unknown GPU"
    if computer:
        try:
            cpu_name = computer.Win32_Processor()[0].Name.strip()
            gpu_name = computer.Win32_VideoController()[0].Name.strip()
        except Exception:
            pass
    return cpu_name, gpu_name

def get_core_counts():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    return f"{cores} Cores / {threads} Threads"

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

# --- NEW: RAM Logic ---
def get_ram_info():
    ram = psutil.virtual_memory()
    total_gb = round(ram.total / (1024 ** 3), 1)
    used_gb = round(ram.used / (1024 ** 3), 1)
    return f"{used_gb} GB / {total_gb} GB ({ram.percent}%)"

# --- NEW: Storage Logic ---
def get_disk_info():
    # Gets info for the main C: drive
    disk = psutil.disk_usage('C:\\')
    total_gb = round(disk.total / (1024 ** 3), 1)
    free_gb = round(disk.free / (1024 ** 3), 1)
    used_gb = round(disk.used / (1024 ** 3), 1)
    return f"{used_gb} GB Used / {free_gb} GB Free ({disk.percent}%)"

def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return get_mock_temp()
        for name, entries in temps.items():
            return round(entries[0].current, 1)
    except AttributeError:
        return get_mock_temp()

def get_gpu_temp(cpu_temp):
    return cpu_temp

def get_mock_temp():
    # Occasionally spikes the temp to test the notification!
    if random.randint(1, 20) == 1:
        return round(random.uniform(80.0, 95.0), 1)
    return round(random.uniform(45.0, 65.0), 1)

def get_health_status(temp):
    if temp < 60:
        return "Optimal 🟢"
    elif temp < 75:
        return "Normal 🟡"
    else:
        return "Critical 🔴"

# --- NEW: Alert System ---
def check_temp_alert(temp):
    global last_alert_time
    current_time = time.time()
    
    # If temp is critical AND we haven't sent an alert in the last 60 seconds
    if temp >= 75.0 and (current_time - last_alert_time) > 60:
        try:
            notification.notify(
                title="Tempooo.io - Thermal Alert!",
                message=f"Warning: System temperature reached {temp}°C!",
                app_name="Tempooo.io",
                timeout=5
            )
            last_alert_time = current_time
        except Exception:
            pass # Failsafe if Windows blocks the notification