from typing import List
import pdfplumber

from models.table import Table
from table_extractors.base import TableExtractor


class PdfPlumberTableExtractor(TableExtractor):
    """
    Extracts tables from a text-based PDF using pdfplumber.
    """

    def extract_tables(self, pdf_path: str) -> List[Table]:
        extracted: List[Table] = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables() or []

                for t_idx, table in enumerate(tables, start=1):
                    # Normalize to strings and strip whitespace
                    rows = [
                        [("" if cell is None else str(cell)).strip() for cell in row]
                        for row in table
                    ]

                    # Skip fully empty tables
                    if not any(any(cell for cell in row) for row in rows):
                        continue

                    extracted.append(
                        Table(page=page_idx, index_on_page=t_idx, rows=rows)
                    )

        return extracted
