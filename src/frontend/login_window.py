import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import USERNAME, PASSWORD, COLORS, FONT_TITLE, FONT_LABEL, FONT_BUTTON

class LoginWindow:
    """Modal login dialog. Sets self.success = True if login passes."""

    def __init__(self, root):
        self.root = root
        self.success = False
        self._build()

    def _build(self):
        self.root.title("Student Management System — Login")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        # Center window
        self.root.geometry("380x280")
        self.root.eval("tk::PlaceWindow . center")

        tk.Label(self.root, text="Student Management System",
                 font=FONT_TITLE, bg=COLORS["bg"], fg=COLORS["fg"]).pack(pady=(30, 5))
        tk.Label(self.root, text="Please log in to continue",
                 font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(0, 20))

        frame = tk.Frame(self.root, bg=COLORS["bg"])
        frame.pack()

        tk.Label(frame, text="Username:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["fg"], width=10, anchor="e").grid(row=0, column=0, pady=6)
        self.user_entry = tk.Entry(frame, font=FONT_LABEL, width=20,
                                   bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        self.user_entry.grid(row=0, column=1, padx=8)

        tk.Label(frame, text="Password:", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["fg"], width=10, anchor="e").grid(row=1, column=0, pady=6)
        self.pass_entry = tk.Entry(frame, font=FONT_LABEL, width=20, show="*",
                                   bg=COLORS["entry_bg"], fg=COLORS["entry_fg"])
        self.pass_entry.grid(row=1, column=1, padx=8)

        tk.Button(self.root, text="Login", font=FONT_BUTTON, width=16,
                  bg=COLORS["accent"], fg="white", relief="flat",
                  command=self._login).pack(pady=20)

        self.root.bind("<Return>", lambda e: self._login())
        self.user_entry.focus()

    def _login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        if u == USERNAME and p == PASSWORD:
            self.success = True
            self.root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.root)
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.focus()
