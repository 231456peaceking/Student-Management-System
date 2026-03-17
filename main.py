import tkinter as tk
import sys, os

# Make src importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from utils.file_paths import ensure_dirs, ensure_files
from frontend.login_window import LoginWindow
from frontend.main_gui import MainGUI

def main():
    ensure_dirs()
    ensure_files()

    # Show login
    login_root = tk.Tk()
    login = LoginWindow(login_root)
    login_root.mainloop()

    if not login.success:
        sys.exit(0)

    # Launch main app
    app = MainGUI()
    app.run()

if __name__ == "__main__":
    main()
