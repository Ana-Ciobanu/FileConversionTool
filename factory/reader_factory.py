from factory.writer_factory import WriterFactory
from readers.txt_reader import TXTReader
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader
from readers.pdf_reader import PDFReader
from readers.docx_reader import DOCXReader
from utils.file_type_detector import FileTypeDetector


class ReaderFactory():

    _READER_MAP = {
        "txt": TXTReader,
        "csv": CSVReader,
        "json": JSONReader,
        "pdf": PDFReader,
        "docx": DOCXReader,
    }

    @staticmethod
    def create(input_format: str, path: str):
        """
        Returns an instance of a FileReader suitable for the input format.

        :param input_format: Target format (e.g. 'txt', 'csv', 'json', 'pdf')
        :param path: Path to the file to be read
        :raises ValueError: If format is not supported
        """
        input_format = input_format.lower()

        reader_cls = ReaderFactory._READER_MAP.get(input_format)

        if not reader_cls:
            raise ValueError(f"Unsupported input format: {input_format}")

        return reader_cls(path)
    
    @classmethod
    def supported_outputs_for_path(cls, input_path: str) -> list[str]:
        ext = FileTypeDetector.get_extension(input_path)
        return cls.supported_outputs_for_extension(ext)

    @classmethod
    def supported_outputs_for_extension(cls, ext: str) -> list[str]:
        ext = (ext or "").lower().lstrip(".")
        reader_cls = cls._READER_MAP.get(ext)
        if not reader_cls:
            return []
        output_type = getattr(reader_cls, "output_type", "")
        return WriterFactory.formats_supporting(output_type)
