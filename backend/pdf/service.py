from pathlib import Path
from pypdf import PdfReader, PdfWriter

from PIL import Image
import io


def merge_pdfs(file_paths, output_path):
    """
    Merge multiple PDF files into a single PDF using PdfWriter.
    
    Args:
        file_paths (list of str or Path): List of PDF file paths to merge.
        output_path (str or Path): Path to save the merged PDF.
    """
    writer = PdfWriter()

    for pdf_path in file_paths:
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            writer.add_page(page)

    # Save merged PDF
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


def split_pdf(file_path, output_dir):
    """
    Split a PDF file into separate pages, each page becomes a PDF.
    
    Args:
        file_path (str or Path): Caminho do PDF original.
        output_dir (str or Path): Diretório onde os PDFs separados serão salvos.
    
    Returns:
        List[Path]: Lista com os caminhos dos PDFs gerados.
    """
    reader = PdfReader(str(file_path))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files = []

    for i, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = output_dir / f"{file_path.stem}_page_{i}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)

        output_files.append(output_path)

    return output_files


def compress_pdf(input_path: Path, output_path: Path, image_quality: int = 20, max_dim: int = 1200):
    """
    Compress a PDF by recompressing images inside it using Pillow (JPEG).
    
    Args:
        input_path (Path): Original PDF path.
        output_path (Path): Path to save compressed PDF.
        image_quality (int): JPEG quality for images (1-100).
        max_dim (int): Maximum dimension (width/height) for images.
    """
    reader = PdfReader(str(input_path))
    writer = PdfWriter()
    writer._compress = True

    for page_num, page in enumerate(reader.pages, start=1):
        # Iterate over images in the page (if any)
        if "/XObject" in page["/Resources"]:
            xobjects = page["/Resources"]["/XObject"].get_object()
            for name in list(xobjects.keys()):
                xobj = xobjects[name]
                if xobj["/Subtype"] == "/Image":
                    try:
                        # Extract image data
                        data = xobj.get_data()
                        mode = "RGB"
                        if xobj["/ColorSpace"] == "/DeviceCMYK":
                            mode = "CMYK"
                        elif xobj["/ColorSpace"] == "/DeviceGray":
                            mode = "L"

                        img = Image.open(io.BytesIO(data)).convert(mode)

                        # Resize if larger than max_dim
                        if img.width > max_dim or img.height > max_dim:
                            img.thumbnail((max_dim, max_dim))

                        # Recompress image
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format="JPEG", quality=image_quality, optimize=True)
                        img_bytes.seek(0)

                        # Replace image in PDF
                        xobj._data = img_bytes.read()
                    except Exception as e:
                        # If something fails, keep original image
                        print(f"Warning: failed to compress image on page {page_num}: {e}")
                        continue
        
        writer.add_page(page)

    # Remove all metadata to reduce size
    writer.add_metadata({})

    # Save compressed PDF
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path

