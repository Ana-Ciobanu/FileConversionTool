from core.document_converter import DocumentConverter
from core.pdf_tables_to_csv import PdfTablesToCsvService
from factory.reader_factory import ReaderFactory


class FileConversionFacade:
    def __init__(self, converter: DocumentConverter = None, pdf_table_service: PdfTablesToCsvService = None):
        self.converter = converter if converter is not None else DocumentConverter()
        self.pdf_table_service = pdf_table_service if pdf_table_service is not None else PdfTablesToCsvService()

    def extract_pdf_tables_to_csv(self, pdf_path, output_dir, base_filename=None):
        return self.pdf_table_service.extract_all(pdf_path, output_dir, base_filename)

    def convert_file(self, input_path, output_format, output_path=None):
        return self.converter.convert_file(input_path, output_format, output_path)

    def convert_folder(self, folder_path, output_format, output_dir=None):
        return self.converter.convert_folder(folder_path, output_format, output_dir)
    
    def supported_output_formats(self, input_path: str) -> list[str]:
        return ReaderFactory.supported_outputs_for(input_path)
