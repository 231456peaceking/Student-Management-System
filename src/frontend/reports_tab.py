import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_LABEL, FONT_BUTTON
from utils.file_paths import REPORTS_DIR
from backend.python_bridge.cpp_connector import run
from backend.python_bridge.data_validator import validate_roll

class ReportsTab(tk.Frame):
    """Reports tab: generate and view individual student report cards."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["panel"])
        self._build()

    def _build(self):
        # ── Controls ──────────────────────────────────────────
        ctrl = tk.Frame(self, bg=COLORS["panel"])
        ctrl.pack(fill="x", padx=15, pady=(12, 6))

        tk.Label(ctrl, text="Roll Number:", font=FONT_LABEL,
                 bg=COLORS["panel"], fg=COLORS["fg"]).pack(side="left", padx=(0,6))
        self.roll_entry = tk.Entry(ctrl, font=FONT_LABEL, width=10,
                                   bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        self.roll_entry.pack(side="left", padx=(0,12))

        tk.Button(ctrl, text="Generate Report", font=FONT_BUTTON, width=16,
                  bg=COLORS["green"], fg="white", relief="flat",
                  command=self._generate).pack(side="left", padx=6)
        tk.Button(ctrl, text="List Reports", font=FONT_BUTTON, width=14,
                  bg=COLORS["accent"], fg="white", relief="flat",
                  command=self._list_reports).pack(side="left", padx=6)

        # ── Report list ───────────────────────────────────────
        self.listbox = tk.Listbox(self, font=FONT_LABEL, height=6,
                                  bg=COLORS["entry_bg"], fg=COLORS["entry_fg"],
                                  selectbackground=COLORS["accent"])
        self.listbox.pack(fill="x", padx=15, pady=(0,6))
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # ── Report viewer ─────────────────────────────────────
        tk.Label(self, text="Report Preview:", font=FONT_LABEL,
                 bg=COLORS["panel"], fg=COLORS["fg"]).pack(anchor="w", padx=15)
        self.viewer = scrolledtext.ScrolledText(self, font=("Courier", 11), height=16,
                                                bg=COLORS["entry_bg"], fg=COLORS["entry_fg"],
                                                state="disabled")
        self.viewer.pack(fill="both", expand=True, padx=15, pady=(0,10))

        self._list_reports()

    def _generate(self):
        roll_ok, roll = validate_roll(self.roll_entry.get())
        if not roll_ok: messagebox.showerror("Validation", roll); return
        try:
            path = run(["generate_report", roll, REPORTS_DIR])
            messagebox.showinfo("Success", f"Report saved to:\n{path}")
            self._list_reports()
            self._show_file(path)
        except RuntimeError as ex:
            messagebox.showerror("Error", str(ex))

    def _list_reports(self):
        """Populate listbox with all report files in reports directory."""
        self.listbox.delete(0, tk.END)
        if not os.path.exists(REPORTS_DIR):
            return
        for f in sorted(os.listdir(REPORTS_DIR)):
            if f.endswith(".txt"):
                self.listbox.insert(tk.END, f)

    def _on_select(self, _event):
        sel = self.listbox.curselection()
        if not sel: return
        fname = self.listbox.get(sel[0])
        self._show_file(os.path.join(REPORTS_DIR, fname))

    def _show_file(self, path):
        """Display file contents in the viewer."""
        try:
            with open(path) as f:
                content = f.read()
            self.viewer.config(state="normal")
            self.viewer.delete("1.0", tk.END)
            self.viewer.insert(tk.END, content)
            self.viewer.config(state="disabled")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
