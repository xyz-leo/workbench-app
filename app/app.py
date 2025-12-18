from flask import Flask, render_template
from pathlib import Path
import sys

# -----------------------------
# Base directories
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent   # app/
PROJECT_ROOT = BASE_DIR.parent               # workbench-app/

DATA_DIR = PROJECT_ROOT / "data"
TEMP_DIR = PROJECT_ROOT / "temp"

sys.path.append(str(PROJECT_ROOT))
from backend.pdf.routes import pdf_bp
from backend.image.routes import image_bp

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
# Register blueprints
# -----------------------------
app.register_blueprint(pdf_bp)    # PDF processing blueprint
app.register_blueprint(image_bp)  # Image processing blueprint

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/pdf-tools")
def pdf_tools():
    return render_template("pdf_tools.html")

@app.route("/image-tools")
def image_tools():
    return render_template("image_tools.html")

# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )

