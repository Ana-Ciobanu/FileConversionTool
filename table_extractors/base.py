from abc import ABC, abstractmethod
from typing import List
from models.table import Table


class TableExtractor(ABC):
    @abstractmethod
    def extract_tables(self, pdf_path: str) -> List[Table]:
        pass
