import json
from writers.base_writer import FileWriter


class JSONWriter(FileWriter):
    """
    Writes data to a .json file.
    Supports both table and JSON input formats.
    """

    supported_input_types = {"json", "table", "text"}

    def write(self, data: dict, output_path: str):
        payload = {}

        if data.get("type") == "json":
            payload = data.get("data")

        elif data.get("type") == "table":
            payload = {"rows": data.get("rows", [])}

        elif data.get("type") == "text":
            payload = {"content": data.get("content", "")}

        else:
            raise ValueError("Unsupported data type for JSONWriter")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
