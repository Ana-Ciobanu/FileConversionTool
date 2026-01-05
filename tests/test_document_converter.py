from core.document_converter import DocumentConverter


def test_convert_txt_to_json(tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("Hello conversion")

    output_file = tmp_path / "output.json"

    converter = DocumentConverter()
    result = converter.convert_file(
        input_path=str(input_file), output_format="json", output_path=str(output_file)
    )

    assert output_file.exists()
    assert result == str(output_file)


def test_convert_folder(tmp_path):
    # Create input files
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"
    file1.write_text("one")
    file2.write_text("two")

    output_dir = tmp_path / "out"

    converter = DocumentConverter()
    results = converter.convert_folder(
        folder_path=str(tmp_path), output_format="json", output_dir=str(output_dir)
    )

    assert len(results) == 2
    assert (output_dir / "a.json").exists()
    assert (output_dir / "b.json").exists()
