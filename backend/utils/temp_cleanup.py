# backend/utils/temp_cleanup.py

from pathlib import Path
import shutil


def cleanup_temp_dir(path: Path) -> None:
    """
    Remove a temporary working directory and all its contents.

    This should be called after a response using files inside this directory
    has been created (e.g. send_file).
    """
    try:
        if path.exists():
            shutil.rmtree(path)
    except Exception as e:
        print(e)
        # Intentionally silent: cleanup failure should not
        # break the main application flow
        pass
