from abc import ABC, abstractmethod


class FileWriter(ABC):
    @abstractmethod
    def write(self, data: dict, output_path: str):
        pass
