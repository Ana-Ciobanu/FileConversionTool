
from core.document_converter import DocumentConverter
from core.pdf_tables_to_csv import PdfTablesToCsvService

class FileConversionFacade:
    def __init__(self):
        self.converter = DocumentConverter()
        self.pdf_table_service = PdfTablesToCsvService()

    def extract_pdf_tables_to_csv(self, pdf_path, output_dir, base_filename=None):
        """
        Extract all tables from a PDF into CSV files (one CSV per table).
        :param pdf_path: Path to the PDF file
        :param output_dir: Directory to save CSV files
        :param base_filename: Optional base name for output files
        :return: List of output CSV file paths
        """
        return self.pdf_table_service.extract_all(pdf_path, output_dir, base_filename)

    def convert_file(self, input_path, output_format, output_path=None):
        return self.converter.convert_file(
            input_path=input_path,
            output_format=output_format,
            output_path=output_path
        )

    def convert_folder(self, folder_path, output_format, output_dir=None):
        return self.converter.convert_folder(
            folder_path=folder_path,
            output_format=output_format,
            output_dir=output_dir
        )