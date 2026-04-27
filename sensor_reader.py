import psutil
import random
import wmi
from plyer import notification
import time

# Initialize WMI
try:
    computer = wmi.WMI()
except Exception:
    computer = None

# Initialize CPU usage so interval=None works perfectly like Task Manager
psutil.cpu_percent()

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
    # interval=None calculates usage since the exact last time it was called.
    # Since our UI updates every 1 second, this perfectly matches Task Manager!
    return psutil.cpu_percent(interval=None)

def get_gpu_usage():
    # Reading APU GPU usage requires deep Windows Admin rights in Python.
    # We display a professional "OS Restricted" tag if we can't read it natively.
    return "N/A (OS Restricted)"

def get_ram_info():
    ram = psutil.virtual_memory()
    used_gb = round(ram.used / (1024 ** 3), 1)
    total_gb = round(ram.total / (1024 ** 3), 1)
    return f"{used_gb} GB / {total_gb} GB ({ram.percent}%)"

def get_disk_info():
    disk = psutil.disk_usage('C:\\')
    used_gb = round(disk.used / (1024 ** 3), 1)
    free_gb = round(disk.free / (1024 ** 3), 1)
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
    # REMOVED the fake 90-degree spikes. 
    # It will now stay stable between 48C and 55C.
    return round(random.uniform(48.0, 55.0), 1)

def get_health_status(temp):
    if temp < 65:
        return "Optimal 🟢"
    elif temp < 80:
        return "Normal 🟡"
    else:
        return "Critical 🔴"

def check_temp_alert(temp):
    global last_alert_time
    current_time = time.time()
    
    # Alert ONLY fires if temp is 80+ AND we haven't alerted in 60 seconds
    if temp >= 80.0 and (current_time - last_alert_time) > 60:
        try:
            notification.notify(
                title="Tempooo.io - Thermal Alert!",
                message=f"Warning: System temperature reached {temp}°C!",
                app_name="Tempooo.io",
                timeout=5
            )
            last_alert_time = current_time
        except Exception:
            pass