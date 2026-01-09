import csv
import logging
from readers.base_reader import FileReader


class CSVReader(FileReader):
    output_type = "table"

    def __init__(self, path):
        self.path = path

    def read(self):
        rows = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(row)
        except Exception as e:
            logging.error(f"Failed to read CSV file {self.path}: {e}")
            raise
        return {"type": "table", "rows": rows}
