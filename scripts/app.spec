# a -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path.cwd()
APP_SCRIPT = PROJECT_ROOT / "app" / "app.py"

# -----------------------------
# Hidden imports
# -----------------------------
# ensures all backend modules are included
hidden_imports = collect_submodules("backend")

# -----------------------------
# Datas (extra files)
# -----------------------------
datas = [
    # templates
    (str(PROJECT_ROOT / "app" / "templates"), "templates"),
    # static files
    (str(PROJECT_ROOT / "app" / "static"), "static"),
    # optional data folder
    (str(PROJECT_ROOT / "data"), "data"),
    # optional temp folder
    (str(PROJECT_ROOT / "temp"), "temp"),
]

# -----------------------------
# Build
# -----------------------------
block_cipher = None

a = Analysis(
    [str(APP_SCRIPT)],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="app",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # True if you want to run in terminal
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="app",
)

