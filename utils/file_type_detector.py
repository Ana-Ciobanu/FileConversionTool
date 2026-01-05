import os


class FileTypeDetector:

    @staticmethod
    def get_extension(file_path: str) -> str:
        """
        Extracts and returns the file extension without the dot.

        Example:
            'report.pdf' -> 'pdf'
            'data.csv'   -> 'csv'

        :param file_path: Path to the file
        :return: File extension in lowercase (without '.')
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower().lstrip(".")
