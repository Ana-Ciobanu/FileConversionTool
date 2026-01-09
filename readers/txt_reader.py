from readers.base_reader import FileReader
import logging


class TXTReader(FileReader):
    output_type = "text"

    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Failed to read TXT file {self.path}: {e}")
            raise
        return {"type": "text", "content": content}
