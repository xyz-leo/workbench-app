from flask import Blueprint, request, send_file, jsonify, after_this_request
from backend.pdf.service import merge_pdfs, split_pdf, compress_pdf
from backend.utils.temp_cleanup import cleanup_temp_dir
from pathlib import Path
import tempfile
import zipfile
import uuid

pdf_bp = Blueprint("pdf", __name__, url_prefix="/pdf-tools")

# -----------------------------
# Temp directory
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMP_DIR = PROJECT_ROOT / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Merge PDF
# -----------------------------
@pdf_bp.route("/merge", methods=["POST"])
def merge_route():
    if "pdfs" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    pdf_files = request.files.getlist("pdfs")
    if len(pdf_files) < 2:
        return jsonify({"error": "Please upload at least two PDFs"}), 400

    # Create isolated work dir
    work_dir = TEMP_DIR / f"pdf_merge_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    file_paths = []
    for f in pdf_files:
        path = work_dir / f.filename
        f.save(path)
        file_paths.append(path)

    output_path = work_dir / "merged.pdf"
    merge_pdfs(file_paths, output_path)

    return send_file(output_path, as_attachment=True, download_name="merged.pdf")


# -----------------------------
# Split PDF
# -----------------------------
@pdf_bp.route("/split", methods=["POST"])
def split_route():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]

    # Create isolated work dir
    work_dir = TEMP_DIR / f"pdf_split_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    pdf_path = work_dir / pdf_file.filename
    pdf_file.save(pdf_path)

    pages = split_pdf(pdf_path, work_dir)

    zip_path = work_dir / f"{pdf_path.stem}_pages.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for page_file in pages:
            zipf.write(page_file, arcname=page_file.name)

    return send_file(zip_path, as_attachment=True, download_name=zip_path.name)


# -----------------------------
# Compress PDF
# -----------------------------
@pdf_bp.route("/compress", methods=["POST"])
def compress_route():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]

    # Create isolated work dir
    work_dir = TEMP_DIR / f"pdf_compress_{uuid.uuid4().hex}"
    work_dir.mkdir(parents=True, exist_ok=True)

    @after_this_request
    def cleanup(response):
        cleanup_temp_dir(work_dir)
        return response

    pdf_path = work_dir / pdf_file.filename
    pdf_file.save(pdf_path)

    output_path = work_dir / f"{pdf_path.stem}_compressed.pdf"

    quality = request.form.get("quality", type=int) or 20

    compress_pdf(pdf_path, output_path, image_quality=quality)

    return send_file(output_path, as_attachment=True, download_name=output_path.name)

