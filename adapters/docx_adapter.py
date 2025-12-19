from docx import Document
from adapters.base_reader import FileReader

class DOCXAdapter(FileReader):
    """
    Reads Microsoft Word (.docx) files and returns their textual content.
    """
    def __init__(self, path):
        self.path = path

    def read(self):
        doc = Document(self.path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        content = "\n".join(paragraphs)

        return {
            "type": "text",
            "content": content
        }
