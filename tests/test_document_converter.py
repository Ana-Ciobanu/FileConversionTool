import os
from core.document_converter import DocumentConverter
from core.conversion_facade import FileConversionFacade


# Helper to create a temp file with content
def create_temp_file(tmp_path, name, content):
    file = tmp_path / name
    file.write_text(content)
    return str(file)


def test_txt_to_json(tmp_path):
    input_file = create_temp_file(tmp_path, "sample.txt", "Hello World")
    output_file = tmp_path / "sample.json"
    converter = DocumentConverter()
    result = converter.convert_file(str(input_file), "json", str(output_file))
    assert os.path.exists(result)
    with open(result, "r", encoding="utf-8") as f:
        assert "Hello World" in f.read()


def test_json_to_txt(tmp_path):
    import json

    data = {"foo": "bar", "num": 42}
    input_file = create_temp_file(tmp_path, "sample.json", json.dumps(data))
    output_file = tmp_path / "sample.txt"
    converter = DocumentConverter()
    result = converter.convert_file(str(input_file), "txt", str(output_file))
    assert os.path.exists(result)
    with open(result, "r", encoding="utf-8") as f:
        content = f.read()
        assert "foo" in content and "bar" in content


def test_facade_supported_formats():
    facade = FileConversionFacade()
    # Should support json, docx, pdf for txt input
    formats = facade.supported_output_formats("foo.txt")
    assert "json" in formats
    assert "docx" in formats
    assert "pdf" in formats


def test_convert_folder(tmp_path):
    file1 = create_temp_file(tmp_path, "a.txt", "one")
    file2 = create_temp_file(tmp_path, "b.txt", "two")
    output_dir = tmp_path / "out"
    converter = DocumentConverter()
    results = converter.convert_folder(str(tmp_path), "json", str(output_dir))
    assert len(results) == 2
    assert os.path.exists(output_dir / "a.json")
    assert os.path.exists(output_dir / "b.json")


def test_transformer_registry():
    from core.transformers.transformer_registry import get_transformer

    transformer = get_transformer("json", "text")
    assert transformer is not None
    data = {"type": "json", "data": {"a": 1}}
    result = transformer.transform(data)
    assert result["type"] == "text"
    assert "a" in result["content"]
