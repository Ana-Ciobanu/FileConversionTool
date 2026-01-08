from readers.base_reader import FileReader


class TXTReader(FileReader):
    supported_outputs = ["pdf", "docx"]

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read()

        return {"type": "text", "content": content}
