import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD
from core.conversion_facade import FileConversionFacade


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # WINDOW CONFIG
        self.title("File Conversion Tool")
        self.geometry("700x500")
        self.minsize(600, 450)
        self.resizable(True, True)

        # CORE
        self.converter = FileConversionFacade()
        self.selected_file = None
        self.selected_folder = None

        # SCROLLABLE CONTAINER
        self.container = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # BUILD UI
        self._build_ui()
        self._enable_drag_and_drop()

    # UI LAYOUT
    def _build_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.container,
            text="File Conversion Tool",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.pack(pady=(10, 20))

        # Drag & Drop Area
        self.drop_label = ctk.CTkLabel(
            self.container,
            text="Drag & Drop a file or folder here",
            fg_color=("gray85", "gray25"),
            corner_radius=10,
            width=500,
            height=80,
        )
        self.drop_label.pack(pady=10)

        # File selection
        self.file_label = ctk.CTkLabel(self.container, text="No file selected")
        self.file_label.pack(pady=(20, 5))

        ctk.CTkButton(
            self.container, text="Select File", command=self.select_file, width=200
        ).pack(pady=5)

        # Folder selection
        self.folder_label = ctk.CTkLabel(self.container, text="No folder selected")
        self.folder_label.pack(pady=(20, 5))

        ctk.CTkButton(
            self.container, text="Select Folder", command=self.select_folder, width=200
        ).pack(pady=5)

        # Output format
        ctk.CTkLabel(
            self.container,
            text="Select output format:",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(30, 5))

        self.format_dropdown = ctk.CTkComboBox(
            self.container, values=["txt", "csv", "json", "pdf", "docx"], width=200
        )
        self.format_dropdown.set("txt")
        self.format_dropdown.pack(pady=5)

        # Convert buttons
        ctk.CTkButton(
            self.container,
            text="Convert Selected File",
            command=self.convert_file,
            width=260,
        ).pack(pady=(30, 10))

        ctk.CTkButton(
            self.container,
            text="Convert Entire Folder",
            command=self.convert_folder,
            width=260,
        ).pack(pady=5)

        # PDF Tables to CSV Button
        ctk.CTkButton(
            self.container,
            text="Extract PDF Tables to CSV",
            command=self.extract_pdf_tables_to_csv,
            width=260,
        ).pack(pady=(20, 10))

        # Status
        self.status_label = ctk.CTkLabel(self.container, text="", wraplength=500)
        self.status_label.pack(pady=(30, 20))

    # DRAG & DROP
    def _enable_drag_and_drop(self):
        # Manually load TkDND (required for CustomTkinter compatibility)
        TkinterDnD._require(self)

        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self._handle_drop)

    def _handle_drop(self, event):
        path = event.data.strip("{}")

        if os.path.isfile(path):
            self.selected_file = path
            self.selected_folder = None
            self.file_label.configure(text=f"File: {os.path.basename(path)}")
            self.folder_label.configure(text="No folder selected")
            self.status_label.configure(text="File selected via drag & drop")

        elif os.path.isdir(path):
            self.selected_folder = path
            self.selected_file = None
            self.folder_label.configure(text=f"Folder: {path}")
            self.file_label.configure(text="No file selected")
            self.status_label.configure(text="Folder selected via drag & drop")

        else:
            messagebox.showerror("Error", "Unsupported drop item")

    # ACTIONS
    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file = path
            self.selected_folder = None
            self.file_label.configure(text=f"File: {os.path.basename(path)}")
            self.folder_label.configure(text="No folder selected")

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_folder = path
            self.selected_file = None
            self.folder_label.configure(text=f"Folder: {path}")
            self.file_label.configure(text="No file selected")

    def convert_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        try:
            output = self.converter.convert_file(
                input_path=self.selected_file, output_format=self.format_dropdown.get()
            )

            self.status_label.configure(text=f"Successfully converted to:\n{output}")
            self._scroll_to_bottom()

        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def convert_folder(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        output_dir = os.path.join(self.selected_folder, "converted")

        try:
            results = self.converter.convert_folder(
                folder_path=self.selected_folder,
                output_format=self.format_dropdown.get(),
                output_dir=output_dir,
            )

            self.status_label.configure(
                text=f"Converted {len(results)} files.\nOutput folder:\n{output_dir}"
            )
            self._scroll_to_bottom()

        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def _scroll_to_bottom(self):
        """
        Automatically scrolls to the bottom of the scrollable frame.
        """
        self.container._parent_canvas.yview_moveto(1.0)

    def extract_pdf_tables_to_csv(self):
        if not self.selected_file or not self.selected_file.lower().endswith(".pdf"):
            messagebox.showerror("Error", "Please select a PDF file first.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory for CSVs")
        if not output_dir:
            return

        try:
            output_files = self.converter.extract_pdf_tables_to_csv(
                pdf_path=self.selected_file,
                output_dir=output_dir
            )
            if output_files:
                msg = f"Extracted {len(output_files)} tables to CSV files:\n" + "\n".join(output_files)
            else:
                msg = "No tables found in the PDF."
            self.status_label.configure(text=msg)
            self._scroll_to_bottom()
        except Exception as e:
            messagebox.showerror("PDF Table Extraction Error", str(e))
