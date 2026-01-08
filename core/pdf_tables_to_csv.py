import os
import csv
from typing import List, Optional

from factory.table_extractor_factory import TableExtractorFactory


class PdfTablesToCsvService:
    """
    Service: Extract all tables from a PDF into CSV files (one CSV per table).
    """

    def __init__(self, engine: str = "pdfplumber"):
        self._extractor = TableExtractorFactory.create(engine)

    def extract_all(
        self,
        pdf_path: str,
        output_dir: str,
        base_filename: Optional[str] = None
    ) -> List[str]:
        """
        Extracts tables from pdf_path and writes them to output_dir as:
        <base>_table_001_p1.csv, <base>_table_002_p3.csv, ...

        :return: list of output CSV paths
        """
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        os.makedirs(output_dir, exist_ok=True)

        tables = self._extractor.extract_tables(pdf_path)
        if not base_filename:
            base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        output_files: List[str] = []

        for global_idx, table in enumerate(tables, start=1):
            filename = f"{base_filename}_table_{global_idx:03d}_p{table.page}.csv"
            out_path = os.path.join(output_dir, filename)

            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for row in table.rows:
                    writer.writerow(row)

            output_files.append(out_path)

        return output_files
