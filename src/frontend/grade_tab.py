import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_LABEL, FONT_BUTTON, FONT_TABLE, GRADE_SCALE
from backend.python_bridge.cpp_connector import run
from backend.python_bridge.data_validator import validate_roll, validate_mark

def _grade_color(grade):
    return COLORS.get(grade, COLORS["fg"])

class GradeTab(tk.Frame):
    """Grade management: enter marks, auto-calculate grade, view all grades."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["panel"])
        self._build()
        self.refresh_table()

    def _build(self):
        # ── Form ──────────────────────────────────────────────
        form = tk.LabelFrame(self, text=" Enter Grades ", font=FONT_LABEL,
                             bg=COLORS["panel"], fg=COLORS["fg"], padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=(12, 6))

        fields = [("Roll Number", 8), ("Math (0-100)", 8),
                  ("English (0-100)", 8), ("Science (0-100)", 8)]
        self.entries = {}
        for i, (lbl, w) in enumerate(fields):
            tk.Label(form, text=lbl + ":", font=FONT_LABEL,
                     bg=COLORS["panel"], fg=COLORS["fg"]).grid(row=0, column=i*2, padx=(10,2), sticky="e")
            e = tk.Entry(form, font=FONT_LABEL, width=w,
                         bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
            e.grid(row=0, column=i*2+1, padx=(0,8))
            e.bind("<KeyRelease>", self._auto_calc)
            self.entries[lbl] = e

        # Auto-calculated display
        calc = tk.Frame(form, bg=COLORS["panel"])
        calc.grid(row=1, column=0, columnspan=8, pady=(8,0))

        tk.Label(calc, text="Total:", font=FONT_LABEL, bg=COLORS["panel"], fg=COLORS["fg"]).pack(side="left", padx=6)
        self.lbl_total = tk.Label(calc, text="—", font=FONT_LABEL, bg=COLORS["panel"], fg=COLORS["accent"], width=5)
        self.lbl_total.pack(side="left")

        tk.Label(calc, text="Percentage:", font=FONT_LABEL, bg=COLORS["panel"], fg=COLORS["fg"]).pack(side="left", padx=6)
        self.lbl_pct = tk.Label(calc, text="—", font=FONT_LABEL, bg=COLORS["panel"], fg=COLORS["accent"], width=8)
        self.lbl_pct.pack(side="left")

        tk.Label(calc, text="Grade:", font=FONT_LABEL, bg=COLORS["panel"], fg=COLORS["fg"]).pack(side="left", padx=6)
        self.lbl_grade = tk.Label(calc, text="—", font=("Helvetica", 13, "bold"),
                                  bg=COLORS["panel"], fg=COLORS["accent"], width=4)
        self.lbl_grade.pack(side="left")

        # ── Buttons ───────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=COLORS["panel"])
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Save Grades", font=FONT_BUTTON, width=12,
                  bg=COLORS["green"], fg="white", relief="flat",
                  command=self._save).pack(side="left", padx=6)
        tk.Button(btn_frame, text="View Student", font=FONT_BUTTON, width=12,
                  bg=COLORS["accent"], fg="white", relief="flat",
                  command=self._view_one).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Refresh All", font=FONT_BUTTON, width=12,
                  bg=COLORS["panel"], fg="white", relief="flat",
                  command=self.refresh_table).pack(side="left", padx=6)

        # ── Table ─────────────────────────────────────────────
        cols = ("Roll", "Math", "English", "Science", "Total", "Percentage", "Grade")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        widths = [80, 80, 90, 90, 80, 100, 70]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15,0), pady=8)
        scroll.pack(side="left", fill="y", pady=8)

    def _auto_calc(self, _event=None):
        """Recalculate total, percentage, grade whenever a mark field changes."""
        try:
            m = int(self.entries["Math (0-100)"].get())
            e = int(self.entries["English (0-100)"].get())
            s = int(self.entries["Science (0-100)"].get())
            if not all(0 <= v <= 100 for v in [m, e, s]):
                raise ValueError
            total = m + e + s
            pct = total / 300 * 100
            grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
            self.lbl_total.config(text=str(total))
            self.lbl_pct.config(text=f"{pct:.1f}%")
            self.lbl_grade.config(text=grade, fg=_grade_color(grade))
        except ValueError:
            self.lbl_total.config(text="—")
            self.lbl_pct.config(text="—")
            self.lbl_grade.config(text="—", fg=COLORS["accent"])

    def refresh_table(self):
        """Reload all grades from backend."""
        self.tree.delete(*self.tree.get_children())
        try:
            data = run(["view_grades"])
            for line in data.splitlines():
                if not line: continue
                parts = line.split("|")
                if len(parts) == 4:
                    roll, m, e, s = parts
                    total = int(m) + int(e) + int(s)
                    pct = total / 300 * 100
                    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
                    row = (roll, m, e, s, total, f"{pct:.1f}%", grade)
                    iid = self.tree.insert("", "end", values=row)
                    self.tree.tag_configure(grade, foreground=_grade_color(grade))
                    self.tree.item(iid, tags=(grade,))
        except RuntimeError:
            pass

    def _save(self):
        roll_ok, roll = validate_roll(self.entries["Roll Number"].get())
        if not roll_ok: messagebox.showerror("Validation", roll); return

        m_ok, m = validate_mark(self.entries["Math (0-100)"].get(), "Math")
        if not m_ok: messagebox.showerror("Validation", m); return

        e_ok, e = validate_mark(self.entries["English (0-100)"].get(), "English")
        if not e_ok: messagebox.showerror("Validation", e); return

        s_ok, s = validate_mark(self.entries["Science (0-100)"].get(), "Science")
        if not s_ok: messagebox.showerror("Validation", s); return

        try:
            run(["add_grades", roll, m, e, s])
            messagebox.showinfo("Success", "Grades saved.")
            self.refresh_table()
        except RuntimeError as ex:
            messagebox.showerror("Error", str(ex))

    def _view_one(self):
        roll_ok, roll = validate_roll(self.entries["Roll Number"].get())
        if not roll_ok: messagebox.showerror("Validation", roll); return
        try:
            data = run(["view_student_grades", roll])
            self.tree.delete(*self.tree.get_children())
            parts = data.split("|")
            if len(parts) == 4:
                r, m, e, s = parts
                total = int(m) + int(e) + int(s)
                pct = total / 300 * 100
                grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "D" if pct >= 60 else "F"
                self.tree.insert("", "end", values=(r, m, e, s, total, f"{pct:.1f}%", grade))
        except RuntimeError as ex:
            messagebox.showerror("Not Found", str(ex))
