from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from writers.base_writer import FileWriter


class PDFWriter(FileWriter):
    """
    Writes text content to a PDF file.
    Supports text-based data only.
    """

    supported_input_types = {"text"}

    def write(self, data: dict, output_path: str):
        if data.get("type") != "text":
            raise ValueError("PDFWriter supports only text data")

        content = data.get("content", "")

        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        x_margin = 40
        y_position = height - 40

        for line in content.split("\n"):
            if y_position <= 40:
                c.showPage()
                y_position = height - 40

            c.drawString(x_margin, y_position, line)
            y_position -= 14

        c.save()
