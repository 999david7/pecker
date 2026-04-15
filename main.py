import tkinter as tk
from datetime import datetime, timedelta
import threading
import time

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        # Theme colors (clean modern)
        self.bg = "#0b1220"
        self.card = "#121a2b"
        self.accent = "#4f9cff"
        self.text = "#e6edf3"
        self.muted = "#7c8594"

        self.root.configure(bg=self.bg)

        self.alarms = []

        # Container
        self.container = tk.Frame(root, bg=self.bg)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Clock
        self.time_label = tk.Label(self.container,
                                   font=("Segoe UI", 48, "bold"),
                                   fg=self.accent,
                                   bg=self.bg)
        self.time_label.pack(pady=(10, 20))

        # Card
        self.card_frame = tk.Frame(self.container, bg=self.card)
        self.card_frame.pack(fill="x", pady=10)

        # Entry
        self.entry = tk.Entry(self.card_frame,
                              font=("Segoe UI", 14),
                              justify="center",
                              bd=0,
                              bg="#1c2538",
                              fg=self.text,
                              insertbackground="white")
        self.entry.pack(fill="x", padx=15, pady=15, ipady=8)

        # Buttons
        btn_frame = tk.Frame(self.card_frame, bg=self.card)
        btn_frame.pack(pady=(0, 10))

        self.make_button(btn_frame, "Add", self.add_alarm).grid(row=0, column=0, padx=5)
        self.make_button(btn_frame, "Clear", self.clear_alarms, "#ff5c5c").grid(row=0, column=1, padx=5)
        self.make_button(btn_frame, "Snooze", self.snooze, "#f59e0b").grid(row=0, column=2, padx=5)

        # Alarm list
        self.listbox = tk.Listbox(self.container,
                                 font=("Segoe UI", 12),
                                 bg=self.card,
                                 fg=self.text,
                                 selectbackground=self.accent,
                                 bd=0,
                                 highlightthickness=0)
        self.listbox.pack(fill="both", expand=True, pady=15)

        # Status
        self.status = tk.Label(self.container,
                               text="Ready",
                               font=("Segoe UI", 10),
                               bg=self.bg,
                               fg=self.muted)
        self.status.pack()

        self.update_clock()
        self.start_checker()

    def make_button(self, parent, text, cmd, color=None):
        return tk.Button(parent,
                         text=text,
                         command=cmd,
                         bg=color or self.accent,
                         fg="white",
                         activebackground="#3b82f6",
                         relief="flat",
                         font=("Segoe UI", 10, "bold"),
                         padx=12,
                         pady=6,
                         bd=0,
                         cursor="hand2")

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def add_alarm(self):
        t = self.entry.get()
        if t and t not in self.alarms:
            self.alarms.append(t)
            self.listbox.insert(tk.END, t)
            self.status.config(text=f"Added {t}", fg="#22c55e")
            self.entry.delete(0, tk.END)
        else:
            self.status.config(text="Invalid or duplicate", fg="#ef4444")

    def clear_alarms(self):
        self.alarms.clear()
        self.listbox.delete(0, tk.END)
        self.status.config(text="Cleared", fg=self.muted)

    def snooze(self):
        t = (datetime.now() + timedelta(minutes=5)).strftime("%H:%M:%S")
        self.alarms.append(t)
        self.listbox.insert(tk.END, t)
        self.status.config(text=f"Snoozed to {t}", fg="#facc15")

    def start_checker(self):
        def loop():
            while True:
                now = datetime.now().strftime("%H:%M:%S")
                if now in self.alarms:
                    self.trigger(now)
                time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()

    def trigger(self, t):
        self.status.config(text=f"⏰ {t}", fg="#facc15")

        popup = tk.Toplevel(self.root)
        popup.geometry("280x140")
        popup.configure(bg=self.card)
        popup.attributes("-topmost", True)

        tk.Label(popup, text="⏰ Alarm",
                 font=("Segoe UI", 18, "bold"),
                 bg=self.card,
                 fg=self.accent).pack(pady=20)

        self.make_button(popup, "Dismiss", popup.destroy).pack()

        for _ in range(4):
            self.root.configure(bg="#1c2538")
            time.sleep(0.15)
            self.root.configure(bg=self.bg)
            time.sleep(0.15)

        if t in self.alarms:
            i = self.alarms.index(t)
            self.alarms.remove(t)
            self.listbox.delete(i)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()