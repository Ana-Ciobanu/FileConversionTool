from abc import ABC, abstractmethod


class ConverterFactory(ABC):

    @abstractmethod
    def create(output_format: str):
        pass
