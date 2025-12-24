# Workbench

Workbench is a **local-first utility web application** that provides a small set of practical, everyday tools through a clean web interface.

It runs as a local web app using a Python backend and a minimal HTML/CSS frontend. How it is used (directly via Python or packaged as an executable) is intentionally left to the user.

The project focuses on simplicity, clarity, and no overengineering.

<img width="346" height="536" alt="Workbench Tools" src="https://github.com/user-attachments/assets/76e0c227-a13e-4e17-91a7-a2d50e30de57" />

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

### To-Do List
- Task management with title and description
- Workspace-based organization
- JSON-based persistence

The To-Do List module is a fully functional frontend-backend component of the Workbench app, designed to help users manage tasks organized by workspaces. It allows users to create multiple workspaces, add, edit, and delete tasks within each workspace, and maintain a structured overview of their work.  

On the frontend, the module is implemented using a single HTML template (`todo.html`) styled consistently with the main site theme. The layout follows a clear hierarchy: at the top, users can select the current workspace or create/delete workspaces using an interactive panel. Below the workspace selector, there is an expandable "Add Task" panel, allowing users to enter a task title and description.

Tasks are displayed in a collapsible `<details>` format, showing only the title by default. Clicking a task expands it to reveal its description and a "Delete" button. Each task is associated with the currently selected workspace, and task operations are dynamically updated using JavaScript.  

The frontend state mirrors the backend JSON storage. Workspaces and tasks are persisted in a `todo.json` file located in the `data` directory. All CRUD operations (create, read, update, delete) are handled via API endpoints in Flask, providing a seamless and reactive experience. Additionally, the module uses `localStorage` to remember the last selected workspace, ensuring continuity when the user reloads the page or returns later.  

Key features include:

- Multiple workspace management (create, delete, switch)
- Expandable Add Task panel with title and description fields
- Collapsible task list per workspace
- Task deletion with confirmation prompts
- Persistent backend storage in JSON
- Frontend state synchronization with backend via API
- Last workspace selection remembered using browser localStorage

<img width="346" height="581" alt="Workbench To do list" src="https://github.com/user-attachments/assets/a4e78727-5853-4f4e-8c80-7d2f5a84fbc2" />

### PDF Tools
- Merge PDFs
- Split PDFs
- All processing done locally
- Compress PDFs (image recompression, metadata cleanup)

⚠️ **Disclaimer:** In rare cases, some pages may appear blurred after compression. Please review the resulting PDF carefully before use.

### Image Tools
- Image resizing (custom sizes and presets)
- Filter addition (B&W, Sepia, Invert colors, Blur)
- All processing done locally

## Video Tools

The **Video Tools** feature provides simple, server-side video processing through a web interface. It allows users to merge multiple videos into a single file and optionally add background music, without previews or in-browser editing.

The workflow is request-based and fully stateless. Each operation is processed in an isolated temporary directory and discarded after the response is sent.

### Supported operations

- Merge up to **3 MP4 videos** into a single video  
- Optionally add a background music track  
- Control music start time (in seconds)  
- Adjust music volume  

Videos are merged **in alphabetical order by filename**. Users can control the merge order by renaming the files before uploading. Maybe in the future I could add a better control to the merge system.

### How it works

1. The frontend collects video files and optional music parameters and sends them as `multipart/form-data`.
2. The backend saves all files into a temporary, request-scoped directory.
3. Videos are merged if more than one is provided.
4. If a music file is present, it is applied to the final video.
5. The resulting file is returned as a download.
6. All temporary files are cleaned up automatically after the response.

### Design notes

- No persistent storage is used.
- No video previews or timeline editing are performed.
- Processing is synchronous and deterministic.
- The feature is designed for simplicity and reliability, not full video editing.

This approach keeps the system lightweight while still supporting common, practical video operations.

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
```
After, you can run the app with `python app/app.py`

Once running, open your browser and access:
http://127.0.0.1:5000

### Option 2 — Package as an Executable (optional)
Workbench can be packaged as a standalone executable using Pyinstaller.

**The steps from the option 1 are still required (venv with requirements.txt).**

Install the PyInstaller:
```bash
pip install pyinstaller
```

To build the executable, run it from the project root:
```
pyinstaller scripts/app.spec
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
│       ├── pdf_tools.html         # PDF tools UI
│       └── image_tools.html       # Image tools UI
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
│   │   ├── resize_service.py      # Image endpoints
│   │   └── filter_service.py      # Image processing logic
│   │
│   └── utils/                     # Shared backend utilities
│       ├── file_lock.py           # Safe concurrent file writes
│       ├── temp_cleanup.py        # Clean temp folder after request
│       └── paths.py               # Centralized path resolution
│
├── data/
│   └── users/                     # User-specific JSON data storage
│
├── temp/                          # Temporary working files
│
├── scripts/
│   ├── app.spec                   # Pyinstaller script to build the app
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
