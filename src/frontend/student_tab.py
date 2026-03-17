import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_LABEL, FONT_BUTTON, FONT_TABLE
from backend.python_bridge.cpp_connector import run
from backend.python_bridge.data_validator import validate_roll, validate_name, validate_contact

class StudentTab(tk.Frame):
    """Student management tab: Add, Update, Delete, Search, View."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["panel"])
        self._build()
        self.refresh_table()

    def _build(self):
        # ── Form ──────────────────────────────────────────────
        form = tk.LabelFrame(self, text=" Student Details ", font=FONT_LABEL,
                             bg=COLORS["panel"], fg=COLORS["fg"], padx=10, pady=8)
        form.pack(fill="x", padx=15, pady=(12, 6))

        labels = ["Roll Number", "Name", "Class", "Contact"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl + ":", font=FONT_LABEL,
                     bg=COLORS["panel"], fg=COLORS["fg"]).grid(row=0, column=i*2, padx=(10,2), sticky="e")
            e = tk.Entry(form, font=FONT_LABEL, width=14,
                         bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
            e.grid(row=0, column=i*2+1, padx=(0,10))
            self.entries[lbl] = e

        # ── Buttons ───────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=COLORS["panel"])
        btn_frame.pack(pady=6)

        buttons = [
            ("Add",    COLORS["green"],   self._add),
            ("Update", COLORS["accent"],  self._update),
            ("Delete", COLORS["red"],     self._delete),
            ("Search", COLORS["yellow"],  self._search),
            ("Clear",  COLORS["panel"],   self._clear),
            ("Refresh",COLORS["accent"],  self.refresh_table),
        ]
        for text, color, cmd in buttons:
            tk.Button(btn_frame, text=text, font=FONT_BUTTON, width=9,
                      bg=color, fg="white", relief="flat",
                      command=cmd).pack(side="left", padx=4)

        # ── Table ─────────────────────────────────────────────
        cols = ("Roll", "Name", "Class", "Contact")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15,0), pady=8)
        scroll.pack(side="left", fill="y", pady=8)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def refresh_table(self):
        """Reload all students from backend into the table."""
        self.tree.delete(*self.tree.get_children())
        try:
            data = run(["view_students"])
            for line in data.splitlines():
                if line:
                    parts = line.split("|")
                    if len(parts) == 4:
                        self.tree.insert("", "end", values=parts)
        except RuntimeError:
            pass  # Empty file is fine

    def _on_select(self, _event):
        """Populate form fields when a table row is clicked."""
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        keys = ["Roll Number", "Name", "Class", "Contact"]
        for k, v in zip(keys, vals):
            self.entries[k].delete(0, tk.END)
            self.entries[k].insert(0, v)

    def _get_fields(self):
        """Read and validate all form fields. Returns dict or None."""
        roll_ok, roll = validate_roll(self.entries["Roll Number"].get())
        if not roll_ok:
            messagebox.showerror("Validation", roll); return None

        name_ok, name = validate_name(self.entries["Name"].get())
        if not name_ok:
            messagebox.showerror("Validation", name); return None

        cls = self.entries["Class"].get().strip()
        if not cls:
            messagebox.showerror("Validation", "Class cannot be empty"); return None

        contact_ok, contact = validate_contact(self.entries["Contact"].get())
        if not contact_ok:
            messagebox.showerror("Validation", contact); return None

        return {"roll": roll, "name": name, "cls": cls, "contact": contact}

    def _add(self):
        f = self._get_fields()
        if not f: return
        try:
            run(["add_student", f["roll"], f["name"], f["cls"], f["contact"]])
            messagebox.showinfo("Success", "Student added successfully.")
            self._clear(); self.refresh_table()
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))

    def _update(self):
        f = self._get_fields()
        if not f: return
        try:
            run(["update_student", f["roll"], f["name"], f["cls"], f["contact"]])
            messagebox.showinfo("Success", "Student updated successfully.")
            self._clear(); self.refresh_table()
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))

    def _delete(self):
        roll_ok, roll = validate_roll(self.entries["Roll Number"].get())
        if not roll_ok:
            messagebox.showerror("Validation", roll); return
        if not messagebox.askyesno("Confirm", f"Delete student with roll {roll}?"):
            return
        try:
            run(["delete_student", roll])
            messagebox.showinfo("Success", "Student deleted.")
            self._clear(); self.refresh_table()
        except RuntimeError as e:
            messagebox.showerror("Error", str(e))

    def _search(self):
        roll_ok, roll = validate_roll(self.entries["Roll Number"].get())
        if not roll_ok:
            messagebox.showerror("Validation", roll); return
        try:
            data = run(["search_student", roll])
            self.tree.delete(*self.tree.get_children())
            parts = data.split("|")
            if len(parts) == 4:
                self.tree.insert("", "end", values=parts)
        except RuntimeError as e:
            messagebox.showerror("Not Found", str(e))

    def _clear(self):
        for e in self.entries.values():
            e.delete(0, tk.END)
