from pathlib import Path
from PIL import Image, ImageFilter, ImageOps


# -----------------------------
# Supported filters
# -----------------------------

SUPPORTED_FILTERS = {
    "grayscale",
    "sepia",
    "invert",
    "blur",
}


def apply_filters(
    input_path: Path,
    output_path: Path,
    *,
    filters: list[str],
    intensity: int,
) -> None:
    """
    Apply one or multiple filters to an image.

    Args:
        input_path (Path): Path to the source image.
        output_path (Path): Path where the processed image will be saved.
        filters (list[str]): List of filter names to apply.
        intensity (int): Filter intensity (0–100).

    Filters are applied in the order provided.
    This function performs no Flask-related work.
    """

    # -----------------------------
    # Validation
    # -----------------------------

    if not filters:
        raise ValueError("At least one filter must be provided")

    invalid = set(filters) - SUPPORTED_FILTERS
    if invalid:
        raise ValueError(f"Invalid filters: {', '.join(sorted(invalid))}")

    if not (0 <= intensity <= 100):
        raise ValueError("Intensity must be between 0 and 100")

    # Normalize intensity to 0.0–1.0
    strength = intensity / 100.0

    # -----------------------------
    # Image processing
    # -----------------------------

    with Image.open(input_path) as img:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")

        for filter_name in filters:

            # -----------------------------
            # Grayscale
            # -----------------------------
            if filter_name == "grayscale":
                gray = ImageOps.grayscale(img)
                img = Image.blend(img.convert("RGB"), gray.convert("RGB"), strength)

            # -----------------------------
            # Sepia
            # -----------------------------
            elif filter_name == "sepia":
                gray = ImageOps.grayscale(img)
                sepia = gray.convert("RGB")

                pixels = sepia.load()
                width, height = sepia.size

                for y in range(height):
                    for x in range(width):
                        r, g, b = sepia.getpixel((x, y))
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        pixels[x, y] = (
                            min(tr, 255),
                            min(tg, 255),
                            min(tb, 255),
                        )

                img = Image.blend(img, sepia, strength)

            # -----------------------------
            # Invert colors
            # -----------------------------
            elif filter_name == "invert":
                inverted = ImageOps.invert(img)
                img = Image.blend(img, inverted, strength)

            # -----------------------------
            # Blur
            # -----------------------------
            elif filter_name == "blur":
                # Scale blur radius from intensity
                radius = 0.1 + (strength * 5.0)
                blurred = img.filter(ImageFilter.GaussianBlur(radius))
                img = Image.blend(img, blurred, strength)

        # -----------------------------
        # Save output
        # -----------------------------
        img.save(output_path)

