import customtkinter as ctk
import sensor_reader

ctk.set_appearance_mode("dark")

class TempoooApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Taller window to fit all the restored data
        self.title("Tempooo.io 2.0 - Full System Monitor")
        self.geometry("450x700") 
        self.resizable(False, False)
        
        bg_color = "#111111"
        frame_color = "#1E1E1E"
        self.configure(fg_color=bg_color)

        font_main = ctk.CTkFont(family="Segoe UI", size=12)
        font_bold = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        
        cpu_name, gpu_name = sensor_reader.get_hardware_names()

        # --- SECTION 1: HARDWARE IDENTIFICATION ---
        id_frame = ctk.CTkFrame(self, fg_color=frame_color, border_width=1, border_color="#333333")
        id_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(id_frame, text="System Hardware", font=font_bold).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(id_frame, text="CPU:", font=font_main, text_color="#AAAAAA").grid(row=1, column=0, sticky="e", padx=5)
        ctk.CTkLabel(id_frame, text=cpu_name, font=font_main).grid(row=1, column=1, sticky="w", padx=5)
        
        ctk.CTkLabel(id_frame, text="GPU:", font=font_main, text_color="#AAAAAA").grid(row=2, column=0, sticky="e", padx=5)
        ctk.CTkLabel(id_frame, text=gpu_name, font=font_main).grid(row=2, column=1, sticky="w", padx=5)

        # --- SECTION 2: SYSTEM LOAD & MEMORY ---
        load_frame = ctk.CTkFrame(self, fg_color=frame_color, border_width=1, border_color="#333333")
        load_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(load_frame, text="Utilization & Storage", font=font_bold).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(load_frame, text="CPU Usage:", font=font_main, text_color="#AAAAAA").grid(row=1, column=0, sticky="e", padx=5)
        self.cpu_usage_lbl = ctk.CTkLabel(load_frame, text="-- %", font=font_main)
        self.cpu_usage_lbl.grid(row=1, column=1, sticky="w", padx=5)

        ctk.CTkLabel(load_frame, text="GPU Usage:", font=font_main, text_color="#AAAAAA").grid(row=2, column=0, sticky="e", padx=5)
        self.gpu_usage_lbl = ctk.CTkLabel(load_frame, text="--", font=font_main)
        self.gpu_usage_lbl.grid(row=2, column=1, sticky="w", padx=5)

        ctk.CTkLabel(load_frame, text="RAM Load:", font=font_main, text_color="#AAAAAA").grid(row=3, column=0, sticky="e", padx=5)
        self.ram_lbl = ctk.CTkLabel(load_frame, text="--", font=font_main)
        self.ram_lbl.grid(row=3, column=1, sticky="w", padx=5)

        ctk.CTkLabel(load_frame, text="Drive (C:):", font=font_main, text_color="#AAAAAA").grid(row=4, column=0, sticky="e", padx=5)
        self.disk_lbl = ctk.CTkLabel(load_frame, text="--", font=font_main)
        self.disk_lbl.grid(row=4, column=1, sticky="w", padx=5)

        # --- SECTION 3: TEMPERATURE SENSORS (Core Temp Style) ---
        temp_frame = ctk.CTkFrame(self, fg_color=frame_color, border_width=1, border_color="#333333")
        temp_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(temp_frame, text="Thermal Readings", font=font_bold).grid(row=0, column=0, columnspan=5, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(temp_frame, text="Sensor", font=font_main, text_color="#AAAAAA").grid(row=1, column=0, padx=10, sticky="w")
        ctk.CTkLabel(temp_frame, text="Live", font=font_bold).grid(row=1, column=1, padx=5)
        ctk.CTkLabel(temp_frame, text="Min", font=font_bold).grid(row=1, column=2, padx=5)
        ctk.CTkLabel(temp_frame, text="Max", font=font_bold).grid(row=1, column=3, padx=5)
        ctk.CTkLabel(temp_frame, text="Load", font=font_bold).grid(row=1, column=4, padx=5)

        self.core_labels = []
        for i in range(6):
            row_idx = i + 2
            ctk.CTkLabel(temp_frame, text=f"Core #{i}:", font=font_main, text_color="#AAAAAA").grid(row=row_idx, column=0, sticky="w", padx=10, pady=2)
            
            temp_lbl = ctk.CTkLabel(temp_frame, text="-- °C", font=font_main)
            temp_lbl.grid(row=row_idx, column=1, padx=5)
            min_lbl = ctk.CTkLabel(temp_frame, text="--", font=font_main)
            min_lbl.grid(row=row_idx, column=2, padx=5)
            max_lbl = ctk.CTkLabel(temp_frame, text="--", font=font_main)
            max_lbl.grid(row=row_idx, column=3, padx=5)
            load_lbl = ctk.CTkLabel(temp_frame, text="--", font=font_main)
            load_lbl.grid(row=row_idx, column=4, padx=5)

            self.core_labels.append({"temp": temp_lbl, "min": min_lbl, "max": max_lbl, "load": load_lbl})

        # --- SECTION 4: SYSTEM HEALTH ---
        health_frame = ctk.CTkFrame(self, fg_color=frame_color, border_width=1, border_color="#333333")
        health_frame.pack(fill="x", padx=10, pady=5)
        
        self.health_lbl = ctk.CTkLabel(health_frame, text="System Health: Assessing...", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        self.health_lbl.pack(pady=10)

        self.update_dashboard()

    def update_dashboard(self):
        # Fetch Data
        self.cpu_usage_lbl.configure(text=f"{sensor_reader.get_cpu_usage()}%")
        self.gpu_usage_lbl.configure(text=sensor_reader.get_gpu_usage())
        self.ram_lbl.configure(text=sensor_reader.get_ram_info())
        self.disk_lbl.configure(text=sensor_reader.get_disk_info())

        overall_temp = sensor_reader.get_overall_temp()
        health = sensor_reader.get_health_status(overall_temp)
        
        if health == "Critical":
            self.health_lbl.configure(text=f"System Health: {health}", text_color="#FF4444")
        elif health == "Normal":
            self.health_lbl.configure(text=f"System Health: {health}", text_color="#FFBB33")
        else:
            self.health_lbl.configure(text=f"System Health: {health}", text_color="#00C851")

        # Update Core Table
        core_data = sensor_reader.get_per_core_data()
        for i in range(6):
            data = core_data[i]
            labels = self.core_labels[i]
            labels["temp"].configure(text=data["temp"])
            labels["min"].configure(text=data["min"])
            labels["max"].configure(text=data["max"])
            labels["load"].configure(text=data["load"])

        self.after(1000, self.update_dashboard)

if __name__ == "__main__":
    app = TempoooApp()
    app.mainloop()