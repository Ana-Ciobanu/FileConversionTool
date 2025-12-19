from utils.file_type_detector import FileTypeDetector


def test_detect_extension_lowercase():
    assert FileTypeDetector.get_extension("report.pdf") == "pdf"


def test_detect_extension_uppercase():
    assert FileTypeDetector.get_extension("DATA.CSV") == "csv"


def test_detect_extension_no_extension():
    assert FileTypeDetector.get_extension("README") == ""
