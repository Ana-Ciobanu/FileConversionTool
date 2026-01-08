from abc import ABC, abstractmethod


class Transformer(ABC):
    """
    Transforms normalized data from one type to another.
    Example: json -> text, table -> text, json -> table, etc.
    """

    @abstractmethod
    def transform(self, data: dict) -> dict:
        pass
