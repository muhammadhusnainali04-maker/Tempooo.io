import customtkinter as ctk
import sensor_reader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TempoooApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Make window taller to fit new data
        self.title("Tempooo.io - System Monitor")
        self.geometry("450x550") 
        self.resizable(False, False)

        # Fetch static hardware names once (they don't change)
        cpu_name, gpu_name = sensor_reader.get_hardware_names()
        cores_threads = sensor_reader.get_core_counts()

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Tempooo.io", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(15, 10))

        # --- HARDWARE INFO SECTION ---
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(pady=5, padx=20, fill="x")
        
        self.cpu_name_label = ctk.CTkLabel(self.info_frame, text=f"CPU: {cpu_name}", font=ctk.CTkFont(size=14, weight="bold"))
        self.cpu_name_label.pack(pady=(10, 2))
        
        self.cores_label = ctk.CTkLabel(self.info_frame, text=f"Architecture: {cores_threads}", font=ctk.CTkFont(size=12))
        self.cores_label.pack(pady=(0, 2))

        self.gpu_name_label = ctk.CTkLabel(self.info_frame, text=f"GPU: {gpu_name}", font=ctk.CTkFont(size=14, weight="bold"))
        self.gpu_name_label.pack(pady=(2, 10))

        # --- LIVE TELEMETRY SECTION ---
        self.telemetry_frame = ctk.CTkFrame(self)
        self.telemetry_frame.pack(pady=10, padx=20, fill="x")

        self.cpu_usage_label = ctk.CTkLabel(self.telemetry_frame, text="CPU Usage: -- %", font=ctk.CTkFont(size=16))
        self.cpu_usage_label.pack(pady=10)

        self.cpu_temp_label = ctk.CTkLabel(self.telemetry_frame, text="CPU Temp: -- °C", font=ctk.CTkFont(size=16))
        self.cpu_temp_label.pack(pady=10)

        self.gpu_temp_label = ctk.CTkLabel(self.telemetry_frame, text="GPU Temp: -- °C", font=ctk.CTkFont(size=16))
        self.gpu_temp_label.pack(pady=10)

        # --- SYSTEM HEALTH SECTION ---
        self.health_frame = ctk.CTkFrame(self)
        self.health_frame.pack(pady=5, padx=20, fill="x")
        
        self.health_label = ctk.CTkLabel(self.health_frame, text="System Health: Assessing...", font=ctk.CTkFont(size=16, weight="bold"))
        self.health_label.pack(pady=10)

        # Start the live update loop
        self.update_dashboard()

    def update_dashboard(self):
        # Fetch live data
        usage = sensor_reader.get_cpu_usage()
        cpu_t = sensor_reader.get_cpu_temp()
        gpu_t = sensor_reader.get_gpu_temp(cpu_t)
        health = sensor_reader.get_health_status(cpu_t)

        # Update UI text
        self.cpu_usage_label.configure(text=f"CPU Usage: {usage} %")
        self.cpu_temp_label.configure(text=f"CPU Temp: {cpu_t} °C")
        self.gpu_temp_label.configure(text=f"GPU Temp: {gpu_t} °C")
        self.health_label.configure(text=f"System Health: {health}")

        # Loop every 1000ms
        self.after(1000, self.update_dashboard)

if __name__ == "__main__":
    app = TempoooApp()
    app.mainloop()