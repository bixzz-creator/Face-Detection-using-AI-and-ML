import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
from utils.search_logs import open_search_window

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Face Tracker")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f7f9fc")
        self.root.resizable(False, False)

        # ====== Top Navigation Bar ======
        navbar = tk.Frame(root, bg="#232946", height=60)
        navbar.pack(side=tk.TOP, fill=tk.X)
        navbar.pack_propagate(False)

        logo = tk.Label(navbar, text="👁️‍🗨️ FaceTracker", font=("Segoe UI", 18, "bold"), bg="#232946", fg="#eebbc3")
        logo.pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(navbar, text="🟡 Idle", font=("Segoe UI", 14, "bold"), bg="#232946", fg="#b8c1ec")
        self.status_label.pack(side=tk.RIGHT, padx=20)

        # ====== Main Content Area ======
        main_area = tk.Frame(root, bg="#f7f9fc")
        main_area.pack(expand=True, fill=tk.BOTH, pady=20)

        # ====== Info Cards ======
        cards_frame = tk.Frame(main_area, bg="#f7f9fc")
        cards_frame.pack(pady=20)

        self.info_card("Visitors Today", "0", "#eebbc3", cards_frame, 0)
        self.info_card("Total Sessions", "0", "#b8c1ec", cards_frame, 1)
        self.info_card("Last Export", "None", "#a7c7e7", cards_frame, 2)

        # ====== Action Buttons ======
        actions_frame = tk.Frame(main_area, bg="#f7f9fc")
        actions_frame.pack(pady=40)

        self.create_button(actions_frame, "▶ Start Video Tracking", "#6ede8a", lambda: self.start_tracking("test_multiple_videos.py"), 0)
        self.create_button(actions_frame, "🎥 Live Webcam Tracking", "#ffd972", lambda: self.start_tracking("test_webcam_live.py"), 1)
        self.create_button(actions_frame, "⛔ Stop Tracking", "#f67280", self.stop_tracking, 2, disabled=True)
        self.create_button(actions_frame, "📁 Export Logs as CSV", "#b8c1ec", self.export_logs, 3)
        self.create_button(actions_frame, "🔍 Search Visitor Logs", "#eebbc3", open_search_window, 4)

        # ====== Footer ======
        footer = tk.Label(root, text="© 2025 | Team IntelligentVision | Hackathon Edition 🚀",
                          font=("Segoe UI", 10, "italic"), bg="#f7f9fc", fg="#232946")
        footer.pack(side=tk.BOTTOM, pady=10)

        self.process = None

    def info_card(self, title, value, color, parent, col):
        card = tk.Frame(parent, bg=color, width=220, height=100)
        card.grid(row=0, column=col, padx=15)
        card.pack_propagate(False)
        tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=color, fg="#232946").pack()
        tk.Label(card, text=value, font=("Segoe UI", 20, "bold"), bg=color, fg="#232946").pack()

    def create_button(self, parent, text, color, command, col, disabled=False):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 12, "bold"), bg=color, fg="#232946",
                        activebackground=color, relief=tk.FLAT, padx=20, pady=10,
                        command=command, cursor="hand2")
        btn.grid(row=0, column=col, padx=10)
        if disabled:
            btn.config(state=tk.DISABLED)
            self.stop_button = btn
        elif "Video" in text:
            self.start_video_button = btn
        elif "Live Webcam" in text:
            self.start_webcam_button = btn

    def start_tracking(self, script_name):
        if self.process:
            return
        self.status_label.config(text="🟢 Running", fg="#6ede8a")
        self.start_video_button.config(state=tk.DISABLED)
        self.start_webcam_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        def run_script():
            self.process = subprocess.Popen(["python", script_name])
            self.process.wait()
            self.status_label.config(text="🟡 Idle", fg="#b8c1ec")
            self.start_video_button.config(state=tk.NORMAL)
            self.start_webcam_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.process = None
        threading.Thread(target=run_script, daemon=True).start()

    def stop_tracking(self):
        if self.process:
            self.process.terminate()
            self.status_label.config(text="🔴 Stopped", fg="#f67280")
            self.start_video_button.config(state=tk.NORMAL)
            self.start_webcam_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.process = None

    def export_logs(self):
        try:
            from utils.export_csv import export_csv
            export_csv()
            messagebox.showinfo("✅ Exported", "CSV logs exported successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Export failed:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
