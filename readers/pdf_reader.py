import pdfplumber
import logging
from readers.base_reader import FileReader


class PDFReader(FileReader):
    output_type = "text"

    def __init__(self, path: str):
        self.path = path

    def read(self) -> dict:
        text_pages = []
        try:
            with pdfplumber.open(self.path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_pages.append(page_text)
        except Exception as e:
            logging.error(f"Failed to read PDF file {self.path}: {e}")
            raise
        content = "\n".join(text_pages)
        return {"type": "text", "content": content}
