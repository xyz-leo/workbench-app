from pathlib import Path
from PIL import Image

# -----------------------------
# Image resize service
# -----------------------------

PRESETS = {
    "1920x1080": (1920, 1080),
    "1280x720": (1280, 720),
    "1080x1080": (1080, 1080),
}


def resize_image(
    input_path: Path,
    output_path: Path,
    *,
    preset: str | None = None,
    width: int | None = None,
    height: int | None = None,
) -> None:
    """
    Resize an image using either a preset or custom dimensions.

    Exactly one strategy must be provided:
    - preset (string key from PRESETS)
    - width and height (both integers)

    This function performs no Flask-related work.
    It only reads an image from disk and writes the resized result.
    """

    # -----------------------------
    # Resolve target size
    # -----------------------------

    if preset:
        if preset not in PRESETS:
            raise ValueError("Invalid resize preset")
        target_size = PRESETS[preset]
    else:
        if not width or not height:
            raise ValueError("Width and height must be provided for custom resize")
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers")
        target_size = (width, height)

    # -----------------------------
    # Image processing
    # -----------------------------

    with Image.open(input_path) as img:
        # Ensure compatibility with JPEG and other formats
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        resized = img.resize(target_size, Image.LANCZOS)
        resized.save(output_path)

