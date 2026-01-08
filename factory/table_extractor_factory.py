from table_extractors.pdfplumber_extractor import PdfPlumberTableExtractor


class TableExtractorFactory:
    _MAP = {
        "pdfplumber": PdfPlumberTableExtractor,
    }

    @staticmethod
    def create(engine: str = "pdfplumber"):
        engine = engine.lower().strip()
        cls = TableExtractorFactory._MAP.get(engine)
        if not cls:
            raise ValueError(f"Unsupported table extraction engine: {engine}")
        return cls()
