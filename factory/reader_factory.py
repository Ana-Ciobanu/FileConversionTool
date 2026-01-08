from readers.txt_reader import TXTReader
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader
from readers.pdf_reader import PDFReader
from readers.docx_reader import DOCXReader
from factory.converter_factory import ConverterFactory
from utils.file_type_detector import FileTypeDetector


class ReaderFactory(ConverterFactory):

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
    def supported_outputs_for(cls, input_path: str) -> list[str]:
        ext = FileTypeDetector.get_extension(input_path)
        reader_cls = cls._READER_MAP.get(ext.lower())
        if not reader_cls:
            return []
        return list(reader_cls.supported_outputs)
