import json
import csv
from readers.txt_reader import TXTReader
from readers.csv_reader import CSVReader
from readers.json_reader import JSONReader


def test_txt_reader_reads_text(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Hello world")

    reader = TXTReader(str(file))
    data = reader.read()

    assert data["type"] == "text"
    assert data["content"] == "Hello world"


def test_csv_reader_reads_rows(tmp_path):
    file = tmp_path / "sample.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["a", "b"])
        writer.writerow(["1", "2"])

    reader = CSVReader(str(file))
    data = reader.read()

    assert data["type"] == "table"
    assert data["rows"] == [["a", "b"], ["1", "2"]]


def test_json_reader_reads_data(tmp_path):
    file = tmp_path / "sample.json"
    payload = {"name": "Alice", "age": 30}
    file.write_text(json.dumps(payload))

    reader = JSONReader(str(file))
    data = reader.read()

    assert data["type"] == "json"
    assert data["data"] == payload
