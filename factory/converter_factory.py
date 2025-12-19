from writers.txt_writer import TXTWriter
from writers.csv_writer import CSVWriter
from writers.json_writer import JSONWriter
from writers.pdf_writer import PDFWriter


class ConverterFactory:
    """
    Factory Method responsible for creating the correct FileWriter
    based on the desired output format.
    """

    _WRITER_MAP = {
        "txt": TXTWriter,
        "csv": CSVWriter,
        "json": JSONWriter,
        "pdf": PDFWriter,
    }

    @staticmethod
    def create(output_format: str):
        """
        Returns an instance of a FileWriter suitable for the output format.

        :param output_format: Target format (e.g. 'txt', 'csv', 'json', 'pdf')
        :raises ValueError: If format is not supported
        """
        output_format = output_format.lower()

        writer_cls = ConverterFactory._WRITER_MAP.get(output_format)

        if not writer_cls:
            raise ValueError(f"Unsupported output format: {output_format}")

        return writer_cls()
