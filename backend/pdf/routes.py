from flask import Blueprint, request, send_file, jsonify
from backend.pdf.service import merge_pdfs, split_pdf
from pathlib import Path
import tempfile
import zipfile

pdf_bp = Blueprint("pdf", __name__, url_prefix="/pdf-tools")


@pdf_bp.route("/merge", methods=["POST"])
def merge_route():
    """
    Receives PDFs via form-data and returns the merged PDF.
    """
    # Check if files were sent
    if "pdfs" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    pdf_files = request.files.getlist("pdfs")
    if len(pdf_files) < 2:
        return jsonify({"error": "Please upload at least two PDFs"}), 400

    # Save files temporarily
    temp_dir = Path(tempfile.mkdtemp())
    file_paths = []
    for f in pdf_files:
        file_path = temp_dir / f.filename
        f.save(file_path)
        file_paths.append(file_path)

    # Output PDF
    output_path = temp_dir / "merged.pdf"
    merge_pdfs(file_paths, output_path)

    # Return PDF for download
    return send_file(output_path, as_attachment=True, download_name="merged.pdf")


@pdf_bp.route("/split", methods=["POST"])
def split_route():
    """
    Receives a PDF via form-data and returns a zip containing all pages.
    """
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]

    # Save PDF temporarily
    temp_dir = Path(tempfile.mkdtemp())
    pdf_path = temp_dir / pdf_file.filename
    pdf_file.save(pdf_path)

    # Split PDF
    pages = split_pdf(pdf_path, temp_dir)

    # Compress all pages into a zip
    zip_path = temp_dir / f"{pdf_path.stem}_pages.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for page_file in pages:
            zipf.write(page_file, arcname=page_file.name)

    # Return the zip
    return send_file(zip_path, as_attachment=True, download_name=zip_path.name)

