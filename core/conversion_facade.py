from core.document_converter import DocumentConverter

class FileConversionFacade:
    def __init__(self):
        self.converter = DocumentConverter()

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