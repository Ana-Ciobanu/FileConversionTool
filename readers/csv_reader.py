import csv
from readers.base_reader import FileReader


class CSVReader(FileReader):

    def __init__(self, path):
        self.path = path

    def read(self):
        rows = []
        with open(self.path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        return {"type": "table", "rows": rows}
