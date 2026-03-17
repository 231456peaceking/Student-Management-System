import subprocess
import os

BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "student_management")

def run_backend(args):

    result = subprocess.run(
        [BACKEND] + args,
        capture_output=True,
        text=True
    )

    if result.returncode != 0 or result.stderr:
        return None

    return result.stdout