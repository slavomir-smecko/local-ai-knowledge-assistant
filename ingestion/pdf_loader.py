import logging

from pypdf import PdfReader

from config import DOCUMENTS_PATH


logger = logging.getLogger(__name__)


def load_pdf(file_path):

    documents = []

    logger.info(
        "Reading PDF: %s",
        file_path.name
    )

    reader = PdfReader(file_path)

    relative_path = str(
        file_path.relative_to(
            DOCUMENTS_PATH
        )
    )

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if not text:
            continue

        documents.append(
            {
                "source": relative_path,
                "type": "pdf",
                "text": text,
                "page": page_number + 1,
            }
        )

    logger.info(
        "Loaded %s pages from %s",
        len(documents),
        file_path.name
    )

    return documents
