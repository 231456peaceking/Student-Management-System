import os

# Root of the project (two levels up from this file)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR      = os.path.join(ROOT, "src", "data")
BACKUP_DIR    = os.path.join(ROOT, "src", "backups")
REPORTS_DIR   = os.path.join(ROOT, "src", "reports")
BUILD_DIR     = os.path.join(ROOT, "build")
BACKEND_EXE   = os.path.join(BUILD_DIR, "student_management")
CONFIG_FILE   = os.path.join(DATA_DIR, "config.ini")
LOG_FILE      = os.path.join(ROOT, "src", "data", "app.log")

def ensure_dirs():
    """Create all required directories if they don't exist."""
    for d in [DATA_DIR, BACKUP_DIR, REPORTS_DIR, BUILD_DIR]:
        os.makedirs(d, exist_ok=True)

def ensure_files():
    """Create empty data files if they don't exist."""
    for f in ["students.txt", "grades.txt", "attendance.txt"]:
        path = os.path.join(DATA_DIR, f)
        if not os.path.exists(path):
            open(path, "w").close()
