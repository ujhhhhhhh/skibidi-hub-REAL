from app import app
import subprocess
import sys
import importlib.util

def ensure_flask_installed():
    if importlib.util.find_spec("flask") is None:
        print("Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("Flask installed.")
    else:
        print("Flask is already installed.")

# Ensure Flask is ready before proceeding
ensure_flask_installed()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
