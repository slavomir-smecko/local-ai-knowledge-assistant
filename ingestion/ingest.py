import logging
import re

from config import (
    DOCUMENTS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from ingestion.pdf_loader import load_pdf


logger = logging.getLogger(__name__)


def normalize_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()



def remove_frontmatter(text):

    """
    Removes YAML frontmatter from markdown files.

    Example removed:

    ---
    title: Example
    description: Something
    ---

    Keeps:

    # Actual content
    """

    if text.startswith("---"):

        parts = text.split(
            "---",
            2
        )

        if len(parts) == 3:

            return parts[2].strip()


    return text



def detect_category(source):

    """
    Determines document category.

    Example:

    external/n8n/file.md
        -> external

    knowledge/linux/file.md
        -> knowledge
    """

    parts = source.split("/")


    if len(parts) > 1:

        return parts[0]


    return "unknown"

def create_document_id(source):

    return (
        source
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_")
        .lower()
    )

def load_markdown_documents():

    return list(
        DOCUMENTS_PATH.rglob("*.md")
    )



def load_pdf_documents():

    return list(
        DOCUMENTS_PATH.rglob("*.pdf")
    )



def read_markdown(file_path):

    relative_path = str(
        file_path.relative_to(
            DOCUMENTS_PATH
        )
    )


    return [
        {
            "source": relative_path,

            "type": "markdown",

            "category": detect_category(
                relative_path
            ),

            "text": file_path.read_text(
                encoding="utf-8"
            ),
        }
    ]



def split_text(text):

    """
    Heading-aware markdown chunking.

    First split by markdown headings.
    Then split large sections.
    """

    sections = re.split(
        r"(?=^#{1,6}\s)",
        text,
        flags=re.MULTILINE,
    )


    chunks = []


    for section in sections:

        section = section.strip()


        if not section:

            continue


        if len(section) <= CHUNK_SIZE:

            chunks.append(
                section
            )

            continue



        start = 0


        while start < len(section):

            end = start + CHUNK_SIZE


            chunks.append(
                section[start:end]
            )


            start = end - CHUNK_OVERLAP



    return chunks



def process_documents():

    files = []


    files.extend(
        load_markdown_documents()
    )


    files.extend(
        load_pdf_documents()
    )


    logger.info(
        "Documents found: %s",
        len(files)
    )


    all_chunks = []


    for file in files:


        if file.suffix.lower() == ".md":

            documents = read_markdown(
                file
            )


        elif file.suffix.lower() == ".pdf":

            documents = load_pdf(
                file
            )


        else:

            continue



        for document in documents:


            text = document["text"]


            if document["type"] == "markdown":

                text = remove_frontmatter(
                    text
                )


            text = normalize_text(
                text
            )



            chunks = split_text(
                text
            )


            logger.info(
                "%s -> %s chunks",
                file.name,
                len(chunks)
            )



            for index, chunk in enumerate(chunks):


                if not chunk.strip():

                    continue



                metadata = {

                    "source": document["source"],

                    "type": document["type"],

                    "category": detect_category(
                        document["source"]
                    ),

                    "document_id": create_document_id(
                        document["source"]
                    ),

                    "chunk": index,

                }



                if "page" in document:

                    metadata["page"] = (
                        document["page"]
                    )



                all_chunks.append(
                    {
                        "text": chunk,

                        "metadata": metadata,
                    }
                )



    logger.info(
        "Total chunks created: %s",
        len(all_chunks)
    )


    return all_chunks
