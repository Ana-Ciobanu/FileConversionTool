import pdfplumber
from readers.base_reader import FileReader


class PDFReader(FileReader):
    output_type = "text"

    def __init__(self, path: str):
        self.path = path

    def read(self) -> dict:
        text_pages = []

        with pdfplumber.open(self.path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)

        content = "\n".join(text_pages)

        return {"type": "text", "content": content}
