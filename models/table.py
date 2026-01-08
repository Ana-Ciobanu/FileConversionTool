from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Table:
    page: int
    index_on_page: int
    rows: List[List[str]]
    title: Optional[str] = None
