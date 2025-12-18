from flask import (
    Blueprint,
    request,
    send_file,
    jsonify,
    after_this_request,
)
from pathlib import Path
import uuid
import zipfile

from backend.image.resize_service import resize_image
from backend.image.filter_service import apply_filters
from backend.utils.temp_cleanup import cleanup_temp_dir


# -----------------------------
# Blueprint
# -----------------------------

image_bp = Blueprint(
    "image",
    __name__,
    url_prefix="/api/image-tools"
)

# -----------------------------
# Paths
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMP_DIR = PROJECT_ROOT / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Limits
# -----------------------------

MAX_FILES = 10


# =========================================================
# Resize route
# =========================================================

@image_bp.route("/resize", methods=["POST"])
def resize_images():
    files = request.files.getlist("files")

    if not files:
        return jsonify({"error": "No files provided"}), 400

    if len(files) > MAX_FILES:
        return jsonify({"error": f"Maximum {MAX_FILES} images allowed"}), 400

    preset = request.form.get("preset")
    width = request.form.get("width", type=int)
    height = request.form.get("height", type=int)

    # -----------------------------
    # Create isolated work directory
    # -----------------------------
    work_dir = TEMP_DIR / f"image_resize_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Guaranteed cleanup AFTER response
    # -----------------------------
    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    output_files = []

    try:
        for file in files:
            suffix = Path(file.filename).suffix

            input_path = work_dir / f"input_{uuid.uuid4().hex}{suffix}"
            output_path = work_dir / f"{Path(file.filename).stem}_resized{suffix}"

            file.save(input_path)

            resize_image(
                input_path=input_path,
                output_path=output_path,
                preset=preset,
                width=width,
                height=height,
            )

            output_files.append(output_path)

        # -----------------------------
        # Single file
        # -----------------------------
        if len(output_files) == 1:
            return send_file(
                output_files[0],
                as_attachment=True,
                download_name=output_files[0].name,
            )

        # -----------------------------
        # Multiple files → zip
        # -----------------------------
        zip_path = work_dir / "resized_images.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in output_files:
                zipf.write(file_path, arcname=file_path.name)

        return send_file(
            zip_path,
            as_attachment=True,
            download_name="resized_images.zip",
        )

    except Exception as e:
        cleanup_temp_dir(work_dir)  # safety net
        return jsonify({"error": str(e)}), 400


# =========================================================
# Filters route
# =========================================================
@image_bp.route("/filters", methods=["POST"])
def apply_image_filters():

    files = request.files.getlist("files")
    filters = request.form.getlist("filters")
    intensity = request.form.get("intensity", type=int)

    if not files:
        return jsonify({"error": "No files provided"}), 400

    if len(files) > MAX_FILES:
        return jsonify({"error": f"Maximum {MAX_FILES} images allowed"}), 400

    if not filters:
        return jsonify({"error": "No filters selected"}), 400

    if intensity is None:
        return jsonify({"error": "Intensity is required"}), 400

    # -----------------------------
    # Create isolated work directory
    # -----------------------------

    work_dir = TEMP_DIR / f"image_filters_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    output_files = []

    try:
        for file in files:
            suffix = Path(file.filename).suffix

            input_path = work_dir / f"input_{uuid.uuid4().hex}{suffix}"
            output_path = work_dir / f"filtered_{file.filename}"

            file.save(input_path)

            apply_filters(
                input_path=input_path,
                output_path=output_path,
                filters=filters,
                intensity=intensity,
            )

            output_files.append(output_path)

        # -----------------------------
        # Single file → direct download
        # -----------------------------

        if len(output_files) == 1:
            response = send_file(
                output_files[0],
                as_attachment=True,
                download_name=output_files[0].name,
            )

        # -----------------------------
        # Multiple files → zip
        # -----------------------------

        else:
            zip_path = work_dir / "filtered_images.zip"

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in output_files:
                    zipf.write(file_path, arcname=file_path.name)

            response = send_file(
                zip_path,
                as_attachment=True,
                download_name="filtered_images.zip",
            )

    except Exception as e:
        cleanup_temp_dir(work_dir)
        return jsonify({"error": str(e)}), 400

    # -----------------------------
    # Guaranteed cleanup
    # -----------------------------

    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    return response
