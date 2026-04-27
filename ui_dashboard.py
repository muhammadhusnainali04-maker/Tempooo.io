import customtkinter as ctk
import sensor_reader

# Set the overall theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TempoooApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Tempooo.io - System Monitor")
        self.geometry("400x300")
        self.resizable(False, False)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Tempooo.io", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # CPU Usage Frame & Label
        self.cpu_usage_frame = ctk.CTkFrame(self)
        self.cpu_usage_frame.pack(pady=10, padx=20, fill="x")
        self.cpu_usage_label = ctk.CTkLabel(self.cpu_usage_frame, text="CPU Usage: -- %", font=ctk.CTkFont(size=16))
        self.cpu_usage_label.pack(pady=10)

        # CPU Temp Frame & Label
        self.cpu_temp_frame = ctk.CTkFrame(self)
        self.cpu_temp_frame.pack(pady=10, padx=20, fill="x")
        self.cpu_temp_label = ctk.CTkLabel(self.cpu_temp_frame, text="CPU Temp: -- °C", font=ctk.CTkFont(size=16))
        self.cpu_temp_label.pack(pady=10)

        # GPU Temp Frame & Label
        self.gpu_temp_frame = ctk.CTkFrame(self)
        self.gpu_temp_frame.pack(pady=10, padx=20, fill="x")
        self.gpu_temp_label = ctk.CTkLabel(self.gpu_temp_frame, text="GPU Temp: -- °C", font=ctk.CTkFont(size=16))
        self.gpu_temp_label.pack(pady=10)

        # Start the live update loop
        self.update_dashboard()

    def update_dashboard(self):
        # 1. Fetch data from your backend file
        usage = sensor_reader.get_cpu_usage()
        cpu_t = sensor_reader.get_cpu_temp()
        gpu_t = sensor_reader.get_gpu_temp(cpu_t)

        # 2. Update the UI text
        self.cpu_usage_label.configure(text=f"CPU Usage: {usage} %")
        self.cpu_temp_label.configure(text=f"CPU Temp: {cpu_t} °C")
        self.gpu_temp_label.configure(text=f"GPU Temp: {gpu_t} °C")

        # 3. Tell the app to run this function again in 1000ms (1 second)
        self.after(1000, self.update_dashboard)

if __name__ == "__main__":
    app = TempoooApp()
    app.mainloop()