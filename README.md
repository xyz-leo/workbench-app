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
│   ├── app.py              # Flask entry point
│   ├── config.py           # App configuration
│   │
│   ├── backend/            # Backend application logic
│   │   ├── __init__.py
│   │   │
│   │   ├── todo/           # To-do feature
│   │   │   ├── routes.py   # HTTP endpoints
│   │   │   ├── service.py  # Business logic
│   │   │   └── storage.py  # JSON persistence
│   │   │
│   │   ├── pdf/            # PDF tools
│   │   │   ├── routes.py   # PDF endpoints
│   │   │   └── service.py  # PDF processing
│   │   │
│   │   ├── image/          # Image tools
│   │   │   ├── routes.py   # Image endpoints
│   │   │   └── service.py  # Image processing
│   │   │
│   │   └── utils/          # Shared helpers
│   │       ├── file_lock.py # Safe file writes
│   │       └── paths.py    # Path resolution
│
├── data/
│   ├── users/              # User data storage
│   │   └── .gitkeep
│
├── temp/
│   └── .gitkeep            # Temporary working files
│
├── static/
│   ├── css/
│   │   └── main.css        # Global styles
│   │
│   ├── js/
│   │   └── main.js         # Minimal frontend logic
│   │
│   └── assets/
│       └── icons/          # UI icons
│
├── templates/
│   ├── base.html           # Base layout
│   ├── index.html          # Main menu
│   ├── todo.html           # To-do UI
│   ├── pdf.html            # PDF tools UI
│   └── image.html          # Image tools UI
│
├── scripts/
│   └── run_local.py        # Local run helper
│
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```
---

## Notes

Workbench is intentionally designed to be **simple and practical** for the end user.

It does not include:
- Authentication or login systems
- Encryption mechanisms
- Public or internet-facing APIs

All features are local-first and focused on everyday usefulness rather than security or scalability concerns.
