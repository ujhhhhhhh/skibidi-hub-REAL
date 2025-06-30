
import subprocess
import sys
import importlib.util
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "skibidi-sigma-ohio-rizz-secret-key-2025"

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    
    # Create all tables
    db.create_all()

# Import routes after app initialization
from app import *  # noqa: F401,F403

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
ensure_flask_installed()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
