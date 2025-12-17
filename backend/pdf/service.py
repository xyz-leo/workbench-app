from pathlib import Path
from pypdf import PdfReader, PdfWriter


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

    # Salva PDF mesclado
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

