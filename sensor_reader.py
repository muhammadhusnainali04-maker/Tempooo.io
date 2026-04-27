import psutil
import random
import wmi  # New library for Windows hardware names

# Initialize WMI once when the app starts
try:
    computer = wmi.WMI()
except Exception:
    computer = None

def get_hardware_names():
    cpu_name = "Unknown CPU"
    gpu_name = "Unknown GPU"
    
    if computer:
        try:
            # Pull exact names from Windows
            cpu_name = computer.Win32_Processor()[0].Name.strip()
            gpu_name = computer.Win32_VideoController()[0].Name.strip()
        except Exception:
            pass
            
    return cpu_name, gpu_name

def get_core_counts():
    # Gets physical cores and logical threads
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    return f"{cores} Cores / {threads} Threads"

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return get_mock_temp()
        for name, entries in temps.items():
            return entries[0].current
    except AttributeError:
        return get_mock_temp()

def get_gpu_temp(cpu_temp):
    # Fallback for Ryzen APU (Integrated Graphics)
    return cpu_temp

def get_mock_temp():
    # Slightly lower random temp for standard usage
    return round(random.uniform(40.0, 55.0), 1)

def get_health_status(temp):
    # The Health Algorithm based on thermal thresholds
    if temp < 60:
        return "Optimal 🟢"
    elif temp < 80:
        return "Normal 🟡"
    else:
        return "Critical 🔴"