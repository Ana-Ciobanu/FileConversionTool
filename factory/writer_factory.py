from writers.txt_writer import TXTWriter
from writers.csv_writer import CSVWriter
from writers.json_writer import JSONWriter
from writers.pdf_writer import PDFWriter
from writers.docx_writer import DOCXWriter


class WriterFactory:
    """
    Factory Method responsible for creating the correct FileWriter
    based on the desired output format.
    """

    _WRITER_MAP = {
        "txt": TXTWriter,
        "csv": CSVWriter,
        "json": JSONWriter,
        "pdf": PDFWriter,
        "docx": DOCXWriter,
    }

    @staticmethod
    def create(output_format: str):
        """
        Returns an instance of a FileWriter suitable for the output format.

        :param output_format: Target format (e.g. 'txt', 'csv', 'json', 'pdf')
        :raises ValueError: If format is not supported
        """
        output_format = output_format.lower()

        writer_cls = WriterFactory._WRITER_MAP.get(output_format)

        if not writer_cls:
            raise ValueError(f"Unsupported output format: {output_format}")

        return writer_cls()

    @classmethod
    def supported_formats(cls) -> list[str]:
        return sorted(cls._WRITER_MAP.keys())

    @classmethod
    def formats_supporting(cls, input_type: str) -> list[str]:
        input_type = (input_type or "").strip().lower()
        formats = []
        for fmt, writer_cls in cls._WRITER_MAP.items():
            if input_type in getattr(writer_cls, "supported_input_types", set()):
                formats.append(fmt)
        return sorted(formats)
