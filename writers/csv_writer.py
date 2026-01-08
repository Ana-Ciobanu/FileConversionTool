import csv
from writers.base_writer import FileWriter


class CSVWriter(FileWriter):
    """
    Writes tabular data to a .csv file.
    """

    supported_input_types = {"table"}

    def write(self, data: dict, output_path: str):
        if data.get("type") != "table":
            raise ValueError("CSVWriter supports only table data")

        rows = data.get("rows", [])

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
