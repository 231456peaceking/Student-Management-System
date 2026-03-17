import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_TITLE, FONT_LABEL
from frontend.student_tab    import StudentTab
from frontend.grade_tab      import GradeTab
from frontend.attendance_tab import AttendanceTab
from frontend.reports_tab    import ReportsTab
from frontend.backup_tab     import BackupTab

class MainGUI:
    """Main application window shown after successful login."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management System")
        self.root.geometry("900x640")
        self.root.configure(bg=COLORS["bg"])
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._apply_style()
        self._build()

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=COLORS["bg"],  borderwidth=0)
        style.configure("TNotebook.Tab",    background=COLORS["panel"], foreground=COLORS["fg"],
                         padding=[14, 6],   font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",          background=[("selected", COLORS["accent"])])
        style.configure("Treeview",         background=COLORS["entry_bg"], foreground=COLORS["entry_fg"],
                         rowheight=24,      fieldbackground=COLORS["entry_bg"],
                         font=("Helvetica", 10))
        style.configure("Treeview.Heading", background=COLORS["accent"], foreground="white",
                         font=("Helvetica", 10, "bold"))
        style.map("Treeview",               background=[("selected", COLORS["accent"])])

    def _build(self):
        # Header
        header = tk.Frame(self.root, bg=COLORS["bg"], pady=8)
        header.pack(fill="x")
        tk.Label(header, text="Student Management System",
                 font=FONT_TITLE, bg=COLORS["bg"], fg=COLORS["fg"]).pack()

        # Notebook tabs
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=10, pady=(0,4))

        tabs = [
            ("Students",   StudentTab),
            ("Grades",     GradeTab),
            ("Attendance", AttendanceTab),
            ("Reports",    ReportsTab),
            ("Backup",     BackupTab),
        ]
        for name, TabClass in tabs:
            frame = TabClass(nb)
            nb.add(frame, text=f"  {name}  ")

        # Status bar
        self.status = tk.Label(self.root,
                               text=f"Logged in as: admin  |  {datetime.now().strftime('%Y-%m-%d')}",
                               font=("Helvetica", 9), bg=COLORS["bg"], fg=COLORS["accent"],
                               anchor="w", padx=12)
        self.status.pack(fill="x", side="bottom")

    def _on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
