import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_LABEL, FONT_BUTTON, FONT_TABLE
from backend.python_bridge.cpp_connector import run
from backend.python_bridge.data_validator import validate_roll, validate_date

class AttendanceTab(tk.Frame):
    """Attendance tab: mark attendance per student per date, view records and percentages."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["panel"])
        self._build()
        self.refresh_table()

    def _build(self):
        # ── Mark Attendance Form ───────────────────────────────
        form = tk.LabelFrame(self, text=" Mark Attendance ", font=FONT_LABEL,
                             bg=COLORS["panel"], fg=COLORS["fg"], padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=(12, 6))

        tk.Label(form, text="Roll Number:", font=FONT_LABEL,
                 bg=COLORS["panel"], fg=COLORS["fg"]).grid(row=0, column=0, padx=(0,4), sticky="e")
        self.roll_entry = tk.Entry(form, font=FONT_LABEL, width=10,
                                   bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        self.roll_entry.grid(row=0, column=1, padx=(0,16))

        tk.Label(form, text="Date (YYYY-MM-DD):", font=FONT_LABEL,
                 bg=COLORS["panel"], fg=COLORS["fg"]).grid(row=0, column=2, padx=(0,4), sticky="e")
        self.date_entry = tk.Entry(form, font=FONT_LABEL, width=14,
                                   bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        self.date_entry.insert(0, str(date.today()))
        self.date_entry.grid(row=0, column=3, padx=(0,16))

        tk.Label(form, text="Status:", font=FONT_LABEL,
                 bg=COLORS["panel"], fg=COLORS["fg"]).grid(row=0, column=4, padx=(0,4), sticky="e")
        self.status_var = tk.StringVar(value="Present")
        tk.OptionMenu(form, self.status_var, "Present", "Absent").grid(row=0, column=5, padx=(0,10))

        # ── Buttons ───────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=COLORS["panel"])
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Mark Attendance", font=FONT_BUTTON, width=16,
                  bg=COLORS["green"], fg="white", relief="flat",
                  command=self._mark).pack(side="left", padx=6)
        tk.Button(btn_frame, text="View % for Student", font=FONT_BUTTON, width=18,
                  bg=COLORS["accent"], fg="white", relief="flat",
                  command=self._view_pct).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Refresh All", font=FONT_BUTTON, width=12,
                  bg=COLORS["panel"], fg="white", relief="flat",
                  command=self.refresh_table).pack(side="left", padx=6)

        # ── Table ─────────────────────────────────────────────
        cols = ("Roll", "Date", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        widths = [100, 160, 120]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        self.tree.tag_configure("Present", foreground=COLORS["green"])
        self.tree.tag_configure("Absent",  foreground=COLORS["red"])

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15,0), pady=8)
        scroll.pack(side="left", fill="y", pady=8)

    def refresh_table(self):
        """Reload all attendance records."""
        self.tree.delete(*self.tree.get_children())
        try:
            data = run(["view_attendance"])
            for line in data.splitlines():
                if not line: continue
                parts = line.split("|")
                if len(parts) == 3:
                    status = parts[2]
                    iid = self.tree.insert("", "end", values=parts)
                    self.tree.item(iid, tags=(status,))
        except RuntimeError:
            pass

    def _mark(self):
        roll_ok, roll = validate_roll(self.roll_entry.get())
        if not roll_ok: messagebox.showerror("Validation", roll); return

        date_ok, d = validate_date(self.date_entry.get())
        if not date_ok: messagebox.showerror("Validation", d); return

        status = self.status_var.get()
        try:
            run(["mark_attendance", roll, d, status])
            messagebox.showinfo("Success", f"Attendance marked: Roll {roll} — {status} on {d}")
            self.refresh_table()
        except RuntimeError as ex:
            messagebox.showerror("Error", str(ex))

    def _view_pct(self):
        roll_ok, roll = validate_roll(self.roll_entry.get())
        if not roll_ok: messagebox.showerror("Validation", roll); return
        try:
            data = run(["attendance_percentage", roll])
            parts = data.split("|")
            if len(parts) == 4:
                _, present, total, pct = parts
                pct_f = float(pct)
                color = COLORS["green"] if pct_f >= 75 else COLORS["red"]
                msg = f"Roll {roll}\nPresent: {present}/{total}\nAttendance: {pct_f:.1f}%"
                messagebox.showinfo("Attendance %", msg)
        except RuntimeError as ex:
            messagebox.showerror("Error", str(ex))
