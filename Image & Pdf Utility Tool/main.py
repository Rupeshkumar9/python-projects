"""
Image & PDF Utility Tool - Entry Point

A comprehensive tool for PDF and image operations including:
- Merge PDFs
- Split PDF (with custom page ranges)
- Convert images to PDF
- Lock PDF (password-protect with AES-256)
- Unlock PDF (remove password protection)
- Resize images
- Crop images (interactive)
- Compress images to target size
"""

from app import ImagePdfToolApp


if __name__ == "__main__":
    app = ImagePdfToolApp()
    # Default window size
    app.geometry("800x530")
    app.minsize(800, 530)
    print("Started Successfully...")
    app.mainloop()
    print("Closing...")

