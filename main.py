import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime, timedelta


class ModernAlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Aura Alarm")
        self.root.geometry("450x650")
        self.root.configure(bg="#0F172A")  # Deep Midnight Blue

        # Style Palette
        self.colors = {
            "bg": "#0F172A",
            "card": "#1E293B",
            "accent": "#38BDF8",  # Sky Blue
            "accent_low": "#0369A1",
            "text": "#F8FAFC",
            "muted": "#94A3B8",
            "danger": "#F43F5E",
            "warning": "#F59E0B"
        }

        self.alarms = []

        # Setup modern fonts
        self.title_font = tkfont.Font(family="Segoe UI Variable", size=50, weight="bold")
        self.sub_font = tkfont.Font(family="Segoe UI", size=12)
        self.btn_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

        self.build_ui()
        self.update_loop()

    def build_ui(self):
        # --- Top Clock Section ---
        self.header = tk.Frame(self.root, bg=self.colors["bg"], pady=30)
        self.header.pack(fill="x")

        self.time_label = tk.Label(
            self.header, text="00:00:00", font=self.title_font,
            fg=self.colors["accent"], bg=self.colors["bg"]
        )
        self.time_label.pack()

        self.date_label = tk.Label(
            self.header, text=datetime.now().strftime("%A, %B %d"),
            font=self.sub_font, fg=self.colors["muted"], bg=self.colors["bg"]
        )
        self.date_label.pack()

        # --- Input Section (The "Glass" Card) ---
        self.input_card = tk.Frame(self.root, bg=self.colors["card"], padx=20, pady=20)
        self.input_card.pack(fill="x", padx=30, pady=10)

        tk.Label(
            self.input_card, text="SET NEW ALARM", font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"], bg=self.colors["card"]
        ).pack(anchor="w", pady=(0, 10))

        # Modern Entry
        self.entry = tk.Entry(
            self.input_card, font=("Segoe UI", 20), justify="center",
            bg="#0F172A", fg=self.colors["text"], insertbackground="white",
            bd=0, highlightthickness=1, highlightbackground="#334155"
        )
        self.entry.pack(fill="x", ipady=10, pady=(0, 15))
        self.entry.insert(0, "HH:MM")
        self.entry.bind("<FocusIn>", lambda e: self.entry.delete(0, tk.END) if self.entry.get() == "HH:MM" else None)

        # Buttons Grid
        btn_frame = tk.Frame(self.input_card, bg=self.colors["card"])
        btn_frame.pack(fill="x")

        self.create_btn(btn_frame, "ADD ALARM", self.add_alarm, self.colors["accent"]).pack(side="left", expand=True,
                                                                                            fill="x", padx=(0, 5))
        self.create_btn(btn_frame, "CLEAR", self.clear_alarms, "#334155").pack(side="left", expand=True, fill="x",
                                                                               padx=(5, 0))

        # --- Alarm List Section ---
        tk.Label(
            self.root, text="ACTIVE ALARMS", font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"], bg=self.colors["bg"]
        ).pack(anchor="w", padx=35, pady=(20, 5))

        self.listbox = tk.Listbox(
            self.root, font=("Segoe UI", 13), bg=self.colors["bg"],
            fg=self.colors["text"], borderwidth=0, highlightthickness=0,
            selectbackground=self.colors["card"], activestyle="none"
        )
        self.listbox.pack(fill="both", expand=True, padx=35, pady=5)

        # Bottom Status
        self.status_bar = tk.Label(
            self.root, text="System Online", font=("Segoe UI", 9),
            bg="#0F172A", fg=self.colors["muted"], pady=10
        )
        self.status_bar.pack(side="bottom")

    def create_btn(self, parent, text, cmd, color):
        btn = tk.Button(
            parent, text=text, command=cmd, font=self.btn_font,
            bg=color, fg="white", activebackground=color,
            activeforeground="white", relief="flat", bd=0,
            cursor="hand2", pady=10
        )
        # Add hover effect
        btn.bind("<Enter>", lambda e: btn.configure(background=self.lighten_color(color)))
        btn.bind("<Leave>", lambda e: btn.configure(background=color))
        return btn

    def lighten_color(self, hex_color):
        """Helper for hover effects."""
        if not hex_color.startswith('#') or len(hex_color) != 7: return hex_color
        return hex_color  # Simplification for demo; normally calculates lighter shade

    def update_loop(self):
        now_dt = datetime.now()
        now_str = now_dt.strftime("%H:%M:%S")
        self.time_label.config(text=now_str)

        # Check Alarms
        if now_str in self.alarms:
            self.trigger_alarm(now_str)

        self.root.after(1000, self.update_loop)

    def add_alarm(self):
        t = self.entry.get()
        try:
            # Validate format
            valid_t = datetime.strptime(t, "%H:%M").strftime("%H:%M:00")
            if valid_t not in self.alarms:
                self.alarms.append(valid_t)
                self.listbox.insert(tk.END, f"  🔔  {valid_t}")
                self.status_bar.config(text=f"Alarm set: {valid_t}", fg=self.colors["accent"])
            self.entry.delete(0, tk.END)
        except:
            self.status_bar.config(text="Use HH:MM format", fg=self.colors["danger"])

    def clear_alarms(self):
        self.alarms.clear()
        self.listbox.delete(0, tk.END)
        self.status_bar.config(text="Alarms cleared", fg=self.colors["muted"])

    def trigger_alarm(self, t):
        self.root.bell()
        top = tk.Toplevel(self.root)
        top.title("Alarm")
        top.geometry("300x200")
        top.configure(bg=self.colors["card"])
        top.attributes("-topmost", True)

        tk.Label(top, text="TIME'S UP", font=self.btn_font, fg=self.colors["accent"], bg=self.colors["card"]).pack(
            pady=(20, 5))
        tk.Label(top, text=t, font=("Segoe UI", 30, "bold"), fg="white", bg=self.colors["card"]).pack(pady=10)

        self.create_btn(top, "DISMISS", top.destroy, self.colors["danger"]).pack(pady=10, padx=20, fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAlarmClock(root)
    root.mainloop()