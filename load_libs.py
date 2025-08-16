import sys
import subprocess

packages = ["exa_py"]

for package in packages:
    try:
        __import__(package)
        print(f"✅ {package} is already installed.")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
        print(f"✅ {package} installed successfully.")
