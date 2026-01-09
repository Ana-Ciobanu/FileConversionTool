import json
import logging
from readers.base_reader import FileReader


class JSONReader(FileReader):
    """
    Reads JSON files and normalizes them into a Python dict.
    """

    output_type = "json"

    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Failed to read JSON file {self.path}: {e}")
            raise
        return {"type": "json", "data": data}
