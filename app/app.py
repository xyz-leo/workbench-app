from flask import Flask, render_template
from pathlib import Path

# -----------------------------
# Base directories
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent          # app/
PROJECT_ROOT = BASE_DIR.parent                     # workbench-app/

DATA_DIR = PROJECT_ROOT / "data"
TEMP_DIR = PROJECT_ROOT / "temp"

# Ensure runtime directories exist
DATA_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Flask app
# -----------------------------

app = Flask(
    __name__,
    template_folder=BASE_DIR / "templates",
    static_folder=BASE_DIR / "static",
)

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )

