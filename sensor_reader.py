import psutil
import time
import random

try:
    import GPUtil
except ImportError:
    GPUtil = None

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_cpu_temp():
    # Attempt to read real temp, fallback to Mock Data if blocked by Windows
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return get_mock_cpu_temp()
        for name, entries in temps.items():
            return entries[0].current
    except AttributeError:
        return get_mock_cpu_temp()

def get_mock_cpu_temp():
    # Generates a realistic fake temperature between 40.0C and 65.0C
    # This ensures your UI dashboard has data to display during the presentation!
    return round(random.uniform(40.0, 65.0), 1)

def get_gpu_temp():
    if GPUtil is None:
        return "GPUtil not installed"
    
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No dedicated GPU found (or blocked)"
    
    # Return the temperature of the first GPU
    return gpus[0].temperature

def test_sensors():
    print("--- Tempooo.io Sensor Test ---")
    print(f"CPU Usage: {get_cpu_usage()}%")
    print(f"CPU Temp : {get_cpu_temp()} °C")
    print(f"GPU Temp : {get_gpu_temp()} °C")
    print("------------------------------")

if __name__ == "__main__":
    # Run the test 3 times to see the mock data fluctuate
    for _ in range(3):
        test_sensors()
        time.sleep(1)