# backend/utils/temp_cleanup.py

from pathlib import Path
import shutil


def cleanup_temp_dir(path: Path) -> None:
    """
    Remove all contents of a temporary directory except `.gitkeep`.
    """
    try:
        if path.exists():
            for item in path.iterdir():
                if item.name == ".gitkeep":
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    except Exception as e:
        print(e)
        # Silent failure
        pass
