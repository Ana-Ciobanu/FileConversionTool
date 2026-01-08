from abc import ABC, abstractmethod


class FileReader(ABC):
    output_type: str = ""  # "text" | "table" | "json"
    
    @abstractmethod
    def read(self):
        pass
