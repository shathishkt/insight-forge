import os

from pypdf import PdfReader

try:
    from docx import Document
except ImportError:
    Document = None


def load_pdf(file_path):
    """
    Extract text from a PDF file.
    """

    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def load_txt(file_path):
    """
    Extract text from a TXT file.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def load_docx(file_path):
    """
    Extract text from a DOCX file.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


def load_document(file_path):
    """
    Load a supported document.
    """

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return load_pdf(file_path)

    elif extension == ".txt":

        return load_txt(file_path)

    elif extension == ".docx":

        return load_docx(file_path)

    else:

        raise ValueError(
            f"Unsupported document type: {extension}"
        )