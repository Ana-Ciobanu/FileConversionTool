import pytest
from factory.writer_factory import WriterFactory
from factory.reader_factory import ReaderFactory
from writers.txt_writer import TXTWriter
from writers.csv_writer import CSVWriter
from writers.json_writer import JSONWriter
from writers.pdf_writer import PDFWriter
from writers.docx_writer import DOCXWriter
from readers.txt_reader import TXTReader
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader
from readers.pdf_reader import PDFReader
from readers.docx_reader import DOCXReader


def test_writer_factory_creates_writers():
    assert isinstance(WriterFactory.create("txt"), TXTWriter)
    assert isinstance(WriterFactory.create("csv"), CSVWriter)
    assert isinstance(WriterFactory.create("json"), JSONWriter)
    assert isinstance(WriterFactory.create("pdf"), PDFWriter)
    assert isinstance(WriterFactory.create("docx"), DOCXWriter)


def test_writer_factory_unsupported_format():
    with pytest.raises(ValueError):
        WriterFactory.create("exe")


def test_reader_factory_creates_readers():
    dummy_path = "dummy.txt"
    assert isinstance(ReaderFactory.create("txt", dummy_path), TXTReader)
    assert isinstance(ReaderFactory.create("csv", dummy_path), CSVReader)
    assert isinstance(ReaderFactory.create("json", dummy_path), JSONReader)
    assert isinstance(ReaderFactory.create("pdf", dummy_path), PDFReader)
    assert isinstance(ReaderFactory.create("docx", dummy_path), DOCXReader)


def test_reader_factory_unsupported_format():
    with pytest.raises(ValueError):
        ReaderFactory.create("exe", "dummy.txt")
