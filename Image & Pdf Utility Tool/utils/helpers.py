"""
Shared utility functions for the Image & PDF Utility Tool.
"""

def center_dialog(dialog, width, height):
    """Center a dialog window on the screen."""
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")


def get_image_filetypes():
    """Return standard image file type tuples for file dialogs."""
    return [
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("PNG files", "*.png"),
        ("BMP files", "*.bmp"),
        ("GIF files", "*.gif"),
    ]


def get_pdf_filetypes():
    """Return PDF file type tuples for file dialogs."""
    return [("PDF files", "*.pdf")]


def get_save_image_filetypes():
    """Return image file type tuples for save dialogs."""
    return [
        ("PNG files", "*.png"),
        ("JPEG files", "*.jpg *.jpeg"),
        ("BMP files", "*.bmp"),
        ("GIF files", "*.gif"),
    ]
