from writers.base_writer import FileWriter
import logging


class TXTWriter(FileWriter):
    """
    Writes text-based content to a .txt file.
    Works with data produced by TXT, DOCX, and PDF adapters.
    """

    supported_input_types = {"text"}

    def write(self, data: dict, output_path: str):
        if data.get("type") != "text":
            raise ValueError("TXTWriter supports only text data")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(data.get("content", ""))
        except Exception as e:
            logging.error(f"Failed to write TXT file {output_path}: {e}")
            raise
