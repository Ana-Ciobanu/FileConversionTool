import pytest
from factory.converter_factory import ConverterFactory
from writers.txt_writer import TXTWriter
from writers.csv_writer import CSVWriter
from writers.json_writer import JSONWriter
from writers.pdf_writer import PDFWriter


def test_factory_creates_txt_writer():
    writer = ConverterFactory.create("txt")
    assert isinstance(writer, TXTWriter)


def test_factory_creates_csv_writer():
    writer = ConverterFactory.create("csv")
    assert isinstance(writer, CSVWriter)


def test_factory_creates_json_writer():
    writer = ConverterFactory.create("json")
    assert isinstance(writer, JSONWriter)


def test_factory_creates_pdf_writer():
    writer = ConverterFactory.create("pdf")
    assert isinstance(writer, PDFWriter)


def test_factory_unsupported_format():
    with pytest.raises(ValueError):
        ConverterFactory.create("exe")
