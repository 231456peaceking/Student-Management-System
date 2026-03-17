import subprocess
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.file_paths import BACKEND_EXE, DATA_DIR
from utils.logger import log_error

def run(args):
    """
    Purpose: Run the C++ backend with given command arguments
    Args:    args - list of strings, e.g. ["add_student", "101", "Alice", "10A", "0712345678"]
    Returns: stdout string on success, raises RuntimeError on failure
    """
    if not os.path.exists(BACKEND_EXE):
        raise RuntimeError("Backend executable not found. Please run setup.py first.")

    result = subprocess.run(
        [BACKEND_EXE, DATA_DIR] + [str(a) for a in args],
        capture_output=True, text=True
    )

    if result.stderr.startswith("ERROR:"):
        msg = result.stderr.replace("ERROR:", "").strip()
        log_error(f"Backend error: {msg}")
        raise RuntimeError(msg)

    return result.stdout.strip()
