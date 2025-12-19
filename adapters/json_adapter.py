import json
from adapters.base_reader import FileReader

class JSONAdapter(FileReader):
    """
    Reads JSON files and normalizes them into a Python dict.
    """
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {
            "type": "json",
            "data": data
        }
