import tkinter as tk
from tkinter import ttk, messagebox
import shutil, os, sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import COLORS, FONT_LABEL, FONT_BUTTON
from utils.file_paths import DATA_DIR, BACKUP_DIR

DATA_FILES = ["students.txt", "grades.txt", "attendance.txt"]

class BackupTab(tk.Frame):
    """Backup/Restore tab: timestamped backups of all data files."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["panel"])
        self._build()
        self._refresh()

    def _build(self):
        btn_frame = tk.Frame(self, bg=COLORS["panel"])
        btn_frame.pack(fill="x", padx=15, pady=(12, 6))

        tk.Button(btn_frame, text="Create Backup", font=FONT_BUTTON, width=16,
                  bg=COLORS["green"], fg="white", relief="flat",
                  command=self._backup).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Restore Selected", font=FONT_BUTTON, width=16,
                  bg=COLORS["accent"], fg="white", relief="flat",
                  command=self._restore).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Delete Selected", font=FONT_BUTTON, width=16,
                  bg=COLORS["red"], fg="white", relief="flat",
                  command=self._delete).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Refresh", font=FONT_BUTTON, width=10,
                  bg=COLORS["panel"], fg="white", relief="flat",
                  command=self._refresh).pack(side="left", padx=6)

        cols = ("Backup Folder", "Created")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        self.tree.heading("Backup Folder", text="Backup Folder")
        self.tree.column("Backup Folder", width=280)
        self.tree.heading("Created", text="Created")
        self.tree.column("Created", width=200, anchor="center")

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15,0), pady=8)
        scroll.pack(side="left", fill="y", pady=8)

    def _refresh(self):
        """List all backup folders sorted newest first."""
        self.tree.delete(*self.tree.get_children())
        if not os.path.exists(BACKUP_DIR):
            return
        folders = sorted(os.listdir(BACKUP_DIR), reverse=True)
        for folder in folders:
            path = os.path.join(BACKUP_DIR, folder)
            if os.path.isdir(path):
                try:
                    ts = datetime.strptime(folder, "backup_%Y%m%d_%H%M%S")
                    created = ts.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    created = "—"
                self.tree.insert("", "end", values=(folder, created))

    def _backup(self):
        """Copy all data files into a new timestamped backup folder."""
        ts = datetime.now().strftime("backup_%Y%m%d_%H%M%S")
        dest = os.path.join(BACKUP_DIR, ts)
        os.makedirs(dest, exist_ok=True)
        for f in DATA_FILES:
            src = os.path.join(DATA_DIR, f)
            if os.path.exists(src):
                shutil.copy(src, dest)
        messagebox.showinfo("Backup", f"Backup created:\n{ts}")
        self._refresh()

    def _selected_folder(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a backup first.")
            return None
        return self.tree.item(sel[0], "values")[0]

    def _restore(self):
        folder = self._selected_folder()
        if not folder: return
        if not messagebox.askyesno("Restore", f"Restore from {folder}?\nThis will overwrite current data."):
            return
        src_dir = os.path.join(BACKUP_DIR, folder)
        for f in DATA_FILES:
            src = os.path.join(src_dir, f)
            if os.path.exists(src):
                shutil.copy(src, DATA_DIR)
        messagebox.showinfo("Restore", "Data restored successfully.")

    def _delete(self):
        folder = self._selected_folder()
        if not folder: return
        if not messagebox.askyesno("Delete", f"Permanently delete backup {folder}?"):
            return
        shutil.rmtree(os.path.join(BACKUP_DIR, folder))
        self._refresh()
