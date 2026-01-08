import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD
from core.conversion_facade import FileConversionFacade


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.title("File Conversion Tool")
        self.geometry("900x720")
        self.minsize(820, 680)
        self.resizable(True, True)

        self.converter = FileConversionFacade()
        self.selected_file: str | None = None
        self.selected_folder: str | None = None
        self.last_generated_dir: str | None = None 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.root_container = ctk.CTkFrame(self, corner_radius=14, fg_color="#EEF2F7")
        self.root_container.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.root_container.grid_columnconfigure(0, weight=1)
        self.root_container.grid_rowconfigure(0, weight=1)

        self.scroll = ctk.CTkScrollableFrame(
            self.root_container,
            corner_radius=14,
            fg_color="transparent",
        )
        self.scroll.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.scroll.grid_columnconfigure(0, weight=1)

        # Build UI inside scrollable frame
        self._build_ui()
        self._enable_drag_and_drop()

        self._update_action_states()
        self._update_open_output_state()
        self._set_status("Ready")

    # UI
    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color="#F7FAFF")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 12))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="File Conversion Tool",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#1F2937",
        )
        title.grid(row=0, column=0, sticky="w", padx=14, pady=14)

        # Input
        self.input_frame = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color="#FFFFFF")
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.input_frame,
            text="Input",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 6))

        self.drop_label = ctk.CTkLabel(
            self.input_frame,
            text="Drag & Drop a file or folder here",
            fg_color="#EAF2FF",
            text_color="#1F2937",
            corner_radius=12,
            height=70,
        )
        self.drop_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 12))

        self.selected_label = ctk.CTkLabel(
            self.input_frame,
            text="Selected: None",
            text_color="#374151",
            wraplength=780,
        )
        self.selected_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=14, pady=(0, 12))

        self.btn_select_file = ctk.CTkButton(
            self.input_frame,
            text="Select File",
            command=self.select_file,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_select_file.grid(row=3, column=0, sticky="ew", padx=(14, 7), pady=(0, 14))

        self.btn_select_folder = ctk.CTkButton(
            self.input_frame,
            text="Select Folder",
            command=self.select_folder,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_select_folder.grid(row=3, column=1, sticky="ew", padx=(7, 14), pady=(0, 14))

        # Output
        self.output_frame = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color="#FFFFFF")
        self.output_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(1, weight=3)

        ctk.CTkLabel(
            self.output_frame,
            text="Output",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 6))

        ctk.CTkLabel(self.output_frame, text="Format:", text_color="#374151").grid(
            row=1, column=0, sticky="w", padx=14, pady=(0, 10)
        )

        self.format_dropdown = ctk.CTkComboBox(
            self.output_frame,
            values=["txt", "csv", "json", "pdf", "docx"],
            width=200,
        )
        self.format_dropdown.set("txt")
        self.format_dropdown.grid(row=1, column=1, sticky="w", padx=14, pady=(0, 10))

        ctk.CTkLabel(self.output_frame, text="Output directory:", text_color="#374151").grid(
            row=2, column=0, sticky="w", padx=14, pady=(0, 14)
        )

        self.output_dir_var = ctk.StringVar(value="")
        self.output_dir_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_dir_var)
        self.output_dir_entry.grid(row=2, column=1, sticky="ew", padx=(14, 300), pady=(0, 14))

        btns = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        btns.grid(row=2, column=1, sticky="e", padx=(0, 14), pady=(0, 14))

        self.btn_browse_output = ctk.CTkButton(
            btns,
            text="Browse",
            width=100,
            command=self.browse_output_dir,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_browse_output.grid(row=0, column=0, padx=(0, 10))

        self.btn_open_output = ctk.CTkButton(
            btns,
            text="Open Output",
            width=120,
            command=self.open_output_dir,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_open_output.grid(row=0, column=1)

        # Actions
        self.actions_frame = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color="#FFFFFF")
        self.actions_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.actions_frame.grid_columnconfigure(0, weight=1)
        self.actions_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.actions_frame,
            text="Actions",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(14, 6))

        self.btn_convert_file = ctk.CTkButton(
            self.actions_frame,
            text="Convert Selected File",
            command=self.convert_file,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_convert_file.grid(row=1, column=0, sticky="ew", padx=(14, 7), pady=(0, 10))

        self.btn_convert_folder = ctk.CTkButton(
            self.actions_frame,
            text="Convert Entire Folder",
            command=self.convert_folder,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_convert_folder.grid(row=1, column=1, sticky="ew", padx=(7, 14), pady=(0, 10))

        self.btn_extract_tables = ctk.CTkButton(
            self.actions_frame,
            text="Extract PDF Tables → CSVs",
            command=self.extract_pdf_tables_to_csv,
            fg_color="#2F6FED",
            hover_color="#245BCA",
            text_color="white",
        )
        self.btn_extract_tables.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 14))

        # Status
        self.status_frame = ctk.CTkFrame(self.scroll, corner_radius=14, fg_color="#F7FAFF")
        self.status_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.status_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            text_color="#111827",
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        self.progress = ctk.CTkProgressBar(self.status_frame, mode="indeterminate")
        self.progress.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 14))
        self.progress.stop()
        self.progress.grid_remove()

    # Drag & Drop
    def _enable_drag_and_drop(self):
        TkinterDnD._require(self)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self._handle_drop)

    def _handle_drop(self, event):
        try:
            paths = list(self.tk.splitlist(event.data))
        except Exception:
            paths = [event.data.strip("{}")]

        if not paths:
            return

        path = paths[0].strip("{}")

        if os.path.isfile(path):
            self.selected_file = path
            self.selected_folder = None
            self._clear_generated_state()
            self._set_selected_label(file_path=path, folder_path=None)
            self._set_status("File selected")

        elif os.path.isdir(path):
            self.selected_folder = path
            self.selected_file = None
            self._clear_generated_state()
            self._set_selected_label(file_path=None, folder_path=path)
            self._set_status("Folder selected")

        else:
            messagebox.showerror("Error", "Unsupported dropped item.")
            return

        self._update_action_states()
        self._update_format_dropdown_for_selection()

    # Selection
    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("Supported", "*.pdf *.docx *.txt *.csv *.json"),
                ("PDF", "*.pdf"),
                ("DOCX", "*.docx"),
                ("Text", "*.txt"),
                ("CSV", "*.csv"),
                ("JSON", "*.json"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        self.selected_file = path
        self.selected_folder = None
        self._clear_generated_state()
        self._set_selected_label(file_path=path, folder_path=None)
        self._set_status("File selected")
        self._update_action_states()
        self._update_format_dropdown_for_selection()

    def select_folder(self):
        path = filedialog.askdirectory(title="Select a folder")
        if not path:
            return

        self.selected_folder = path
        self.selected_file = None
        self._clear_generated_state()
        self._set_selected_label(file_path=None, folder_path=path)
        self._set_status("Folder selected")
        self._update_action_states()
        self._update_format_dropdown_for_selection()


    def _set_selected_label(self, file_path: str | None, folder_path: str | None):
        if file_path:
            self.selected_label.configure(text=f"Selected file: {file_path}")
            self.output_dir_var.set(os.path.dirname(file_path))
        elif folder_path:
            self.selected_label.configure(text=f"Selected folder: {folder_path}")
            self.output_dir_var.set(os.path.join(folder_path, "converted"))
        else:
            self.selected_label.configure(text="Selected: None")

    def _set_output_formats(self, formats: list[str]):
        if not formats:
            formats = ["txt"]

        current = self.format_dropdown.get()
        self.format_dropdown.configure(values=formats)

        if current in formats:
            self.format_dropdown.set(current)
        else:
            self.format_dropdown.set(formats[0])


    def _update_format_dropdown_for_selection(self):
        if self.selected_file:
            formats = self.converter.supported_output_formats(self.selected_file)
            self._set_output_formats(formats)
            return

        if self.selected_folder:
            exts = set(
                os.path.splitext(f)[1].lower().lstrip(".")
                for f in os.listdir(self.selected_folder)
                if os.path.isfile(os.path.join(self.selected_folder, f))
            )

            if not exts:
                self._set_output_formats(["txt"])
                return

            supported_sets = [
                set(FileConversionFacade.supported_output_formats(ext))
                for ext in exts
            ]

            formats = sorted(set.intersection(*supported_sets)) if supported_sets else ["txt"]
            self._set_output_formats(formats)
            return

        self._set_output_formats(["txt"])



    # Output dir / Open Output
    def browse_output_dir(self):
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.output_dir_var.set(path)
            self._set_status("Output directory selected")

    def _resolve_output_dir(self) -> str | None:
        value = self.output_dir_var.get().strip()
        return value if value else None

    def _clear_generated_state(self):
        self.last_generated_dir = None
        self._update_open_output_state()

    def _update_open_output_state(self):
        enabled = bool(self.last_generated_dir and os.path.isdir(self.last_generated_dir))
        self.btn_open_output.configure(state="normal" if enabled else "disabled")

    def _mark_generated(self, output_dir: str):
        self.last_generated_dir = output_dir
        self._update_open_output_state()

    def open_output_dir(self):
        if not self.last_generated_dir:
            messagebox.showinfo("Open Output", "No generated files yet.")
            return
        if not os.path.isdir(self.last_generated_dir):
            messagebox.showerror("Open Output", "The generated output folder no longer exists.")
            self.last_generated_dir = None
            self._update_open_output_state()
            return
        os.startfile(self.last_generated_dir)

    # Actions
    def convert_file(self):
        if not self.selected_file:
            messagebox.showerror("Missing input", "Please select a file first.")
            return

        output_format = self.format_dropdown.get().strip().lower()
        out_dir = self._resolve_output_dir() or os.path.dirname(self.selected_file)

        def task():
            self.after(0, lambda: self._start_work(f"Converting file to {output_format.upper()}..."))
            try:
                base = os.path.splitext(os.path.basename(self.selected_file))[0]
                out_path = os.path.join(out_dir, f"{base}.{output_format}")

                output = self.converter.convert_file(
                    input_path=self.selected_file,
                    output_format=output_format,
                    output_path=out_path,
                )

                self.after(0, lambda: self._mark_generated(out_dir))
                self.after(0, lambda: self._finish_work("Done"))
                self.after(0, lambda: messagebox.showinfo("Success", f"File converted successfully:\n{output}"))

            except Exception as e:
                self.after(0, lambda: self._finish_work("Ready"))
                self.after(0, lambda: messagebox.showerror("Conversion failed", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def convert_folder(self):
        if not self.selected_folder:
            messagebox.showerror("Missing input", "Please select a folder first.")
            return

        output_format = self.format_dropdown.get().strip().lower()
        out_dir = self._resolve_output_dir() or os.path.join(self.selected_folder, "converted")

        def task():
            self.after(0, lambda: self._start_work(f"Converting folder to {output_format.upper()}..."))
            try:
                results = self.converter.convert_folder(
                    folder_path=self.selected_folder,
                    output_format=output_format,
                    output_dir=out_dir,
                )

                if results:
                    self.after(0, lambda: self._mark_generated(out_dir))
                    self.after(0, lambda: self._finish_work("Done"))
                    self.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Success",
                            f"Converted {len(results)} files.\nOutput folder:\n{out_dir}",
                        ),
                    )
                else:
                    self.after(0, lambda: self._finish_work("Ready"))
                    self.after(0, lambda: messagebox.showinfo("No files", "No supported files were found in that folder."))

            except Exception as e:
                self.after(0, lambda: self._finish_work("Ready"))
                self.after(0, lambda: messagebox.showerror("Conversion failed", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def extract_pdf_tables_to_csv(self):
        if not self.selected_file or not self.selected_file.lower().endswith(".pdf"):
            messagebox.showerror("Missing input", "Please select a PDF file first.")
            return

        out_dir = self._resolve_output_dir()
        if not out_dir:
            out_dir = filedialog.askdirectory(title="Select Output Directory for CSVs")
            if not out_dir:
                return
            self.output_dir_var.set(out_dir)

        def task():
            self.after(0, lambda: self._start_work("Extracting tables from PDF..."))
            try:
                output_files = self.converter.extract_pdf_tables_to_csv(
                    pdf_path=self.selected_file,
                    output_dir=out_dir
                )

                if output_files:
                    self.after(0, lambda: self._mark_generated(out_dir))
                    self.after(0, lambda: self._finish_work("Done"))
                    self.after(
                        0,
                        lambda: messagebox.showinfo(
                            "Success",
                            f"Extracted {len(output_files)} tables.\nOutput folder:\n{out_dir}",
                        ),
                    )
                else:
                    self.after(0, lambda: self._finish_work("Ready"))
                    self.after(0, lambda: messagebox.showinfo("No tables", "No tables were found in this PDF."))

            except Exception as e:
                self.after(0, lambda: self._finish_work("Ready"))
                self.after(0, lambda: messagebox.showerror("Extraction failed", str(e)))

        threading.Thread(target=task, daemon=True).start()

    # States
    def _update_action_states(self):
        has_file = bool(self.selected_file)
        has_folder = bool(self.selected_folder)
        is_pdf = bool(self.selected_file and self.selected_file.lower().endswith(".pdf"))

        self.btn_convert_file.configure(state="normal" if has_file else "disabled")
        self.btn_convert_folder.configure(state="normal" if has_folder else "disabled")
        self.btn_extract_tables.configure(state="normal" if is_pdf else "disabled")

    def _set_status(self, text: str):
        self.status_label.configure(text=text)

    def _start_work(self, status_text: str):
        self.btn_convert_file.configure(state="disabled")
        self.btn_convert_folder.configure(state="disabled")
        self.btn_extract_tables.configure(state="disabled")

        self._set_status(status_text)
        self.progress.grid()
        self.progress.start()

    def _finish_work(self, status_text: str):
        self.progress.stop()
        self.progress.grid_remove()
        self._set_status(status_text)
        self._update_action_states()
        self._update_open_output_state()
