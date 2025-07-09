import subprocess
import sys
from pathlib import Path

def install_requirements(requirements_file="requirements.txt"):
    req_path = Path(requirements_file)
    if not req_path.is_file():
        print(f"❌ File '{requirements_file}' not found.")
        return

    with open(req_path, "r") as file:
        packages = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    for package in packages:
        print(f"⬇️ Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✅ All requirements installed successfully!")

if __name__ == "__main__":
    install_requirements()
