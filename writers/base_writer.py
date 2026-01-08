from abc import ABC, abstractmethod


class FileWriter(ABC):
    supported_input_types: set[str] = set()

    @abstractmethod
    def write(self, data: dict, output_path: str):
        pass
