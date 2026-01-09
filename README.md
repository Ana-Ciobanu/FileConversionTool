# File Conversion Tool

A simple Python application that converts files between various formats (TXT, CSV, JSON, PDF, DOCX) with a modern GUI. The project demonstrates the use of two classic design patterns: **Factory Method** and **Facade**.

## Features
- Convert files between TXT, CSV, JSON, PDF, and DOCX formats
- Extract tables from PDFs to CSV files
- Drag-and-drop or browse to select files/folders
- Output directory selection and quick access
- Modern, user-friendly GUI (CustomTkinter)

## Design Patterns Used

### 1. Factory Method
**Where:**
- `factory/reader_factory.py` and `factory/writer_factory.py`

**Why:**
- The Factory Method pattern is used to create the appropriate file reader or writer object based on the file type (e.g., TXT, CSV, JSON, PDF, DOCX) at runtime, without hardcoding class instantiations throughout the code.

**What Problem It Solves:**
- Decouples the creation of file readers/writers from the main logic, making it easy to add support for new formats and maintain the codebase.

### 2. Facade
**Where:**
- `core/conversion_facade.py`

**Why:**
- The Facade pattern provides a simplified interface (`FileConversionFacade`) to the complex subsystems involved in file conversion (reading, writing, transforming, extracting tables, etc.).

**What Problem It Solves:**
- Hides the complexity of the conversion process from the GUI and other client code, making the application easier to use and extend.

## Project Structure
```
FileConversionTool/
├── core/
│   ├── conversion_facade.py
│   ├── document_converter.py
│   ├── pdf_tables_to_csv.py
│   └── transformers/
├── factory/
│   ├── reader_factory.py
│   ├── writer_factory.py
│   └── ...
├── gui/
│   └── app.py
├── models/
├── readers/
├── writers/
├── table_extractors/
├── tests/
├── utils/
├── requirements.txt
└── main.py
```

## How to Run
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the application:**
   ```bash
   py main.py
   ```

## Testing
Basic tests are provided in the `tests/` directory. To run them:
```bash
pytest
```

## Pattern Integration Diagram
```
[GUI (app.py)]
      |
      v
[Facade: FileConversionFacade]
      |
      v
[Factory: ReaderFactory/WriterFactory] ---> [Reader/Writer Implementations]
      |
      v
[Transformers, Table Extractors, etc.]
```

## Python Version
- Requires Python 3.9+

## Notes
- The Factory Method pattern makes it easy to add new file formats: just implement a new reader/writer and register it in the factory.
- The Facade pattern keeps the GUI code clean and focused on user interaction, not conversion logic.
