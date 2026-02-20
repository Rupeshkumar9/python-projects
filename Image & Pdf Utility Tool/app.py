"""
Main application class for the Image & PDF Utility Tool.
"""
import tkinter as tk

from utils.ui_components import create_primary_button, create_title_label, create_subtitle_label, BG_COLOR, FONT_FAMILY
from operations.pdf_operations import merge_pdfs, split_pdf, images_to_pdf, lock_pdf, unlock_pdf
from operations.image_operations import resize_image, crop_image, compress_image


class ImagePdfToolApp(tk.Tk):
    """Main Image & PDF Tool Application - Inherited from TK class."""
    
    def __init__(self):
        super().__init__()
        self.title("Image & PDF Utility Tool")
        self.configure(bg=BG_COLOR)
        self._build_ui()

    def _build_ui(self):
        """Build the main user interface."""
        # Center the main frame
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(expand=True, fill="both", padx=40, pady=40)

        title_label = create_title_label(container, "Image & PDF Utility Tool")
        title_label.pack(pady=(0, 20))

        subtitle_label = create_subtitle_label(container, "Choose an operation:")
        subtitle_label.pack(pady=(0, 15))

        button_frame = tk.Frame(container, bg=BG_COLOR)
        button_frame.pack()

        # Row 1 buttons
        create_primary_button(
            button_frame,
            text="Merge PDFs",
            command=lambda: merge_pdfs(self),
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        create_primary_button(
            button_frame,
            text="Split PDF",
            command=lambda: split_pdf(self),
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        create_primary_button(
            button_frame,
            text="Resize Image",
            command=lambda: resize_image(self),
        ).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Row 2 buttons
        create_primary_button(
            button_frame,
            text="JPG to PDF",
            command=lambda: images_to_pdf(self),
        ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        create_primary_button(
            button_frame,
            text="Crop Image",
            command=lambda: crop_image(self),
        ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        create_primary_button(
            button_frame,
            text="Compress Image",
            command=lambda: compress_image(self),
        ).grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Row 3 buttons
        create_primary_button(
            button_frame,
            text="Lock PDF",
            command=lambda: lock_pdf(self),
        ).grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        create_primary_button(
            button_frame,
            text="Unlock PDF",
            command=lambda: unlock_pdf(self),
        ).grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Footer
        footer = tk.Label(
            container,
            text="Built with Love, Welcome to my tool",
            font=(FONT_FAMILY, 9),
            bg=BG_COLOR,
            fg="#888888",
        )
        footer.pack(pady=(20, 0))
