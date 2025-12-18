# Workbench

Workbench is a **local-first utility web application** that provides a small set of practical, everyday tools through a clean web interface.

It runs as a local web app using a Python backend and a minimal HTML/CSS frontend. How it is used (directly via Python or packaged as an executable) is intentionally left to the user.

The project focuses on simplicity, clarity, and no overengineering.

---

## Purpose

Workbench is designed to be:
- Local-first
- Offline-friendly
- Simple to understand and maintain
- Free from unnecessary abstractions

All data is processed locally, and all state is stored in plain JSON files. No cloud services, no databases, and no frontend frameworks.

---

## Features

### To-Do
- Task management with title and description
- Workspace-based organization
- JSON-based persistence
- Import/export tasks file

### PDF Tools
- Merge PDFs
- Split PDFs
- Basic size reduction (image recompression, metadata cleanup)
- All processing done locally

### Image Tools
- Image resizing (custom sizes and presets)
- Black and white conversion
- Local image processing

---

## Architecture

Workbench follows a **local web app architecture**:

- HTML/CSS frontend
- Minimal Vanilla JavaScript for interaction
- Python backend exposed as a local HTTP API

Frontend and backend communicate exclusively through HTTP requests, even when running locally. This keeps responsibilities clear and allows future expansion (e.g. LAN usage).

---

## Stack

### Backend
- **Python**
- **Flask** — HTTP server and API
- **Pillow** — image processing
- **pypdf** — PDF manipulation

### Frontend
- **HTML**
- **CSS**
- **Vanilla JavaScript** (minimal usage)

### Persistence
- **JSON files**
- No database
- No localStorage
- Data stored in plain, readable files

---

## Design Principles

- No unnecessary abstractions
- No heavy frameworks
- No frontend libraries
- Clear separation of concerns
- Explicit state handling
- Local-first mindset

The project favors readability and maintainability over cleverness.

---

## How to Run

Workbench can be used in two different ways, depending on user preference.

### Option 1 — Run with Python (development / direct usage)

Requirements:
- Python
- `pip`

Steps:

```bash
git clone https://github.com/xyz-leo/workbench-app.git
cd workbench-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

Once running, open your browser and access:
http://127.0.0.1:5000

### Option 2 — Package as an Executable (optional)
Workbench can be packaged as a standalone executable using Pyinstaller.

Requirements:
- Python
- `pip`
- PyInstaller

Install the PyInstaller:
```bash
pip install pyinstaller
```

Build the executable:
```
pyinstaller --noconsole --onefile app/app.py
```

The generated executable will be available in the dist/ directory.

When executed, the server starts locally and can be accessed via the browser at the configured localhost address.

- Note that this step is completely optional.

---

## Project Structure
```
workbench/
│
├── app/
│   ├── app.py                     # Flask application entry point
│   ├── config.py                  # App-level configuration
│   │
│   ├── static/                    # Static files served by Flask
│   │   ├── assets/                # Icons and visual assets
│   │   ├── css/                   # Global application styles
│   │   └── js/                    # Minimal frontend logic
│   │
│   └── templates/                 # Jinja2 HTML templates
│       ├── base.html              # Base layout (header, footer, blocks)
│       ├── index.html             # Main menu / feature selection
│       ├── todo.html              # To-do feature UI
│       ├── pdf_tools.html               # PDF tools UI
│       └── image_tools.html             # Image tools UI
│
├── backend/
│   ├── __init__.py                # Backend package initializer
│   │
│   ├── todo/                      # To-do feature backend
│   │   ├── routes.py              # HTTP API endpoints
│   │   ├── service.py             # Business logic
│   │   └── storage.py             # JSON persistence layer
│   │
│   ├── pdf/                       # PDF tools backend
│   │   ├── routes.py              # PDF endpoints
│   │   └── service.py             # PDF processing logic
│   │
│   ├── image/                     # Image tools backend
│   │   ├── routes.py              # Image endpoints
│   │   ├── resize_service.py              # Image endpoints
│   │   └── filter_service.py             # Image processing logic
│   │
│   └── utils/                     # Shared backend utilities
│       ├── file_lock.py           # Safe concurrent file writes
│       ├── temp_cleanup.py           # Clean temp folder after request
│       └── paths.py               # Centralized path resolution
│
├── data/
│   └── users/                     # User-specific JSON data storage
│
├── temp/                          # Temporary working files
│
├── scripts/
│   └── run_local.py               # Local development runner
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── LICENSE                        # License file
```
---

## Notes

Workbench is intentionally designed to be **simple and practical** for the end user.

It does not include:
- Authentication or login systems
- Encryption mechanisms
- Public or internet-facing APIs

All features are local-first and focused on everyday usefulness rather than security or scalability concerns.
