import subprocess
import sys
import importlib.util

import os
import stat

def make_everything_777(root_dir="."):
    mode = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO  # 0o777
    for dirpath, dirnames, filenames in os.walk(root_dir):
        os.chmod(dirpath, mode)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                os.chmod(filepath, mode)
            except PermissionError:
                print(f"Permission denied for {filepath}")
    print(f"All permissions set to 777 under {os.path.abspath(root_dir)}")

make_everything_777()
def ensure_flask_installed():
    if importlib.util.find_spec("flask") is None:
        print("Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask installed.")
    else:
        print("Flask is already installed.")

# Ensure Flask is ready before proceeding
from app import app
ensure_flask_installed()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
