import os

from utils.file_type_detector import FileTypeDetector
from factory.reader_factory import ReaderFactory
from factory.writer_factory import WriterFactory


class DocumentConverter:
    """
    Central controller responsible for orchestrating the conversion process.
    """

    def convert_file(
        self, input_path: str, output_format: str, output_path: str | None = None
    ) -> str:
        """
        Convert a single file into the target format.

        :param input_path: Path to input file
        :param output_format: Target output format (txt, csv, json, pdf)
        :param output_path: Optional custom output path
        :return: Path to converted file
        """

        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        input_ext = FileTypeDetector.get_extension(input_path)
        reader = ReaderFactory.create(input_ext, input_path)
        normalized_data = reader.read()

        writer = WriterFactory.create(output_format)

        # Build output path
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"{base_name}.{output_format}"

        # Write output
        writer.write(normalized_data, output_path)

        return output_path

    def convert_folder(
        self, folder_path: str, output_format: str, output_dir: str | None = None
    ) -> list[str]:
        """
        Convert all supported files inside a folder.

        :param folder_path: Path to folder containing input files
        :param output_format: Target output format
        :param output_dir: Optional output directory
        :return: List of successfully converted file paths
        """

        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Invalid folder: {folder_path}")

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        converted_files = []

        for filename in os.listdir(folder_path):
            input_path = os.path.join(folder_path, filename)

            if not os.path.isfile(input_path):
                continue

            try:
                base_name = os.path.splitext(filename)[0]
                output_path = (
                    os.path.join(output_dir, f"{base_name}.{output_format}")
                    if output_dir
                    else f"{base_name}.{output_format}"
                )

                result = self.convert_file(
                    input_path=input_path,
                    output_format=output_format,
                    output_path=output_path,
                )

                converted_files.append(result)

            except Exception as e:
                # Skip unsupported or failed files gracefully
                print(f"Skipping {filename}: {e}")

        return converted_files
