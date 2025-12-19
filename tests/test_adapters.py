import json
import csv
from adapters.txt_adapter import TXTAdapter
from adapters.csv_adapter import CSVAdapter
from adapters.json_adapter import JSONAdapter

def test_txt_adapter_reads_text(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Hello world")

    adapter = TXTAdapter(str(file))
    data = adapter.read()

    assert data["type"] == "text"
    assert data["content"] == "Hello world"

def test_csv_adapter_reads_rows(tmp_path):
    file = tmp_path / "sample.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["a", "b"])
        writer.writerow(["1", "2"])

    adapter = CSVAdapter(str(file))
    data = adapter.read()

    assert data["type"] == "table"
    assert data["rows"] == [["a", "b"], ["1", "2"]]

def test_json_adapter_reads_data(tmp_path):
    file = tmp_path / "sample.json"
    payload = {"name": "Alice", "age": 30}
    file.write_text(json.dumps(payload))

    adapter = JSONAdapter(str(file))
    data = adapter.read()

    assert data["type"] == "json"
    assert data["data"] == payload