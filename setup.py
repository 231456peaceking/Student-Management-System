"""
setup.py — Run this once before launching the application.
Compiles the C++ backend and initializes required directories and files.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from src.utils.file_paths import ensure_dirs, ensure_files

def compile_cpp():
    cpp_dir = os.path.join(ROOT, "src", "backend", "cpp")
    print("Compiling C++ backend...")
    result = subprocess.run(["make"], cwd=cpp_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print("Compilation failed:\n", result.stderr)
        sys.exit(1)
    print("C++ backend compiled successfully.")

if __name__ == "__main__":
    ensure_dirs()
    ensure_files()
    compile_cpp()
    print("\nSetup complete. Run the application with:")
    print("  python3 main.py")
