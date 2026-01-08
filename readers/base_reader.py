from abc import ABC, abstractmethod


class FileReader(ABC):
    supported_outputs: list[str] = []
    
    @abstractmethod
    def read(self):
        pass
