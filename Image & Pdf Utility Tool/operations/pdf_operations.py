"""
PDF operations for the Image & PDF Utility Tool.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import PyPDF2

from utils.helpers import center_dialog, get_pdf_filetypes
from utils.ui_components import create_primary_button, create_secondary_button, BG_COLOR, FONT_FAMILY


def merge_pdfs(app):
    """Merge multiple PDF files into one."""
    # filepaths is a tuple containing directory of the selected files
    filepaths = filedialog.askopenfilenames(
        title="Select PDF files to merge",
        filetypes=get_pdf_filetypes(),
    )
    if not filepaths:  # will be executed if no file is selected
        return
    
    output_path = filedialog.asksaveasfilename(
        title="Save merged PDF as",
        defaultextension=".pdf",
        filetypes=get_pdf_filetypes(),
    )
    if not output_path:
        return

    try:
        writer = PyPDF2.PdfWriter()  # writer will contain the merged pdf data
        for path in filepaths:   
            reader = PyPDF2.PdfReader(path)  # reader contain the pdf file data
            for page in reader.pages:
                writer.add_page(page)

        with open(output_path, "wb") as fileobj:
            writer.write(fileobj)  # create a new merged pdf file

        # Show message in GUI
        messagebox.showinfo("Success", f"Merged {len(filepaths)} PDFs into:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge PDFs.\n\n{e}")


def split_pdf(app):
    """Split a PDF file based on custom page ranges."""
    # Select a PDF file
    filepath = filedialog.askopenfilename(
        title="Select a PDF file to split",
        filetypes=get_pdf_filetypes(),
    )
    
    if not filepath:
        return
    
    try:
        # Open the PDF and get page count
        reader = PyPDF2.PdfReader(filepath)
        total_pages = len(reader.pages)
        
        # Create split dialog window
        split_dialog = tk.Toplevel(app)
        split_dialog.title("Split PDF")
        split_dialog.configure(bg=BG_COLOR)
        split_dialog.transient(app)
        split_dialog.grab_set()
        
        # State for managing ranges
        ranges_list = []  # List of dicts: {"frame": frame, "start_entry": entry, "end_entry": entry}
        dragging_state = {"index": None, "widget": None}
        
        # Info frame at the top
        info_frame = tk.Frame(split_dialog, bg=BG_COLOR)
        info_frame.pack(pady=15, padx=20, fill="x")
        
        filename = os.path.basename(filepath)
        file_label = tk.Label(
            info_frame,
            text=f"File: {filename}",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
            fg="#333333",
        )
        file_label.pack()
        
        pages_label = tk.Label(
            info_frame,
            text=f"Total Pages: {total_pages}",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#0078d4",
        )
        pages_label.pack(pady=(5, 0))
        
        instruction_label = tk.Label(
            info_frame,
            text="Add page ranges below. Drag ranges to reorder them.",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#555555",
        )
        instruction_label.pack(pady=(5, 0))
        
        # Scrollable container for ranges
        ranges_container = tk.Frame(split_dialog, bg=BG_COLOR)
        ranges_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Canvas for scrollable area
        canvas = tk.Canvas(ranges_container, bg=BG_COLOR, highlightthickness=0, height=200)
        scrollbar = tk.Scrollbar(ranges_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ensure canvas window width matches canvas
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", configure_canvas)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def update_range_numbers():
            """Update the range numbers after reordering"""
            for i, range_item in enumerate(ranges_list):
                range_item["number_label"].config(text=f"Range {i + 1}:")
        
        def create_range_item(start_val="1", end_val=str(total_pages)):
            """Create a new range input item"""
            range_frame = tk.Frame(scrollable_frame, bg="#e8e8e8", padx=10, pady=8)
            range_frame.pack(fill="x", pady=5, padx=5)
            
            # Drag handle
            drag_handle = tk.Label(
                range_frame,
                text="≡",
                font=(FONT_FAMILY, 14, "bold"),
                bg="#e8e8e8",
                fg="#888888",
                cursor="fleur",
            )
            drag_handle.pack(side="left", padx=(0, 10))
            
            # Range number label
            range_num = len(ranges_list) + 1
            number_label = tk.Label(
                range_frame,
                text=f"Range {range_num}:",
                font=(FONT_FAMILY, 10, "bold"),
                bg="#e8e8e8",
                fg="#333333",
                width=8,
            )
            number_label.pack(side="left", padx=(0, 10))
            
            # Start page
            tk.Label(
                range_frame,
                text="From:",
                font=(FONT_FAMILY, 10),
                bg="#e8e8e8",
                fg="#333333",
            ).pack(side="left", padx=(0, 5))
            
            start_entry = tk.Entry(range_frame, font=(FONT_FAMILY, 10), width=6)
            start_entry.insert(0, start_val)
            start_entry.pack(side="left", padx=(0, 15))
            
            # End page
            tk.Label(
                range_frame,
                text="To:",
                font=(FONT_FAMILY, 10),
                bg="#e8e8e8",
                fg="#333333",
            ).pack(side="left", padx=(0, 5))
            
            end_entry = tk.Entry(range_frame, font=(FONT_FAMILY, 10), width=6)
            end_entry.insert(0, end_val)
            end_entry.pack(side="left", padx=(0, 15))
            
            # Remove button
            def remove_this_range():
                # Find and remove this range from the list
                for i, r in enumerate(ranges_list):
                    if r["frame"] == range_frame:
                        ranges_list.pop(i)
                        range_frame.destroy()
                        update_range_numbers()
                        break
            
            remove_btn = tk.Button(
                range_frame,
                text="✕",
                font=(FONT_FAMILY, 10, "bold"),
                bg="#d9534f",
                fg="white",
                activebackground="#c9302c",
                activeforeground="white",
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=remove_this_range,
            )
            remove_btn.pack(side="right")
            
            # Store the range item
            range_item = {
                "frame": range_frame,
                "start_entry": start_entry,
                "end_entry": end_entry,
                "number_label": number_label,
            }
            ranges_list.append(range_item)
            
            # Drag and drop functionality
            def on_drag_start(event):
                dragging_state["index"] = ranges_list.index(range_item)
                range_frame.config(bg="#cce5ff")
                drag_handle.config(bg="#cce5ff")
                number_label.config(bg="#cce5ff")
            
            def on_drag_motion(event):
                if dragging_state["index"] is None:
                    return
                
                # Get mouse position relative to scrollable_frame
                y = event.widget.winfo_rooty() + event.y - scrollable_frame.winfo_rooty()
                
                # Find target position
                target_index = None
                for i, r in enumerate(ranges_list):
                    frame_y = r["frame"].winfo_y()
                    frame_h = r["frame"].winfo_height()
                    if y < frame_y + frame_h // 2:
                        target_index = i
                        break
                
                if target_index is None:
                    target_index = len(ranges_list) - 1
                
                # Move the item if needed
                current_index = dragging_state["index"]
                if current_index != target_index:
                    # Reorder the list
                    item = ranges_list.pop(current_index)
                    ranges_list.insert(target_index, item)
                    dragging_state["index"] = target_index
                    
                    # Repack all frames in new order
                    for r in ranges_list:
                        r["frame"].pack_forget()
                    for r in ranges_list:
                        r["frame"].pack(fill="x", pady=5, padx=5)
                    
                    update_range_numbers()
            
            def on_drag_end(event):
                range_frame.config(bg="#e8e8e8")
                drag_handle.config(bg="#e8e8e8")
                number_label.config(bg="#e8e8e8")
                dragging_state["index"] = None
            
            # Bind drag events to the drag handle
            drag_handle.bind("<ButtonPress-1>", on_drag_start)
            drag_handle.bind("<B1-Motion>", on_drag_motion)
            drag_handle.bind("<ButtonRelease-1>", on_drag_end)
            
            return range_item
        
        # Add initial range
        create_range_item()
        
        # Add Range button frame
        add_btn_frame = tk.Frame(split_dialog, bg=BG_COLOR)
        add_btn_frame.pack(pady=10)
        
        def add_new_range():
            create_range_item()
            # Scroll to bottom
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)
        
        add_range_btn = tk.Button(
            add_btn_frame,
            text="+ Add Range",
            font=(FONT_FAMILY, 10),
            bg="#5cb85c",
            fg="white",
            activebackground="#449d44",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=add_new_range,
        )
        add_range_btn.pack()
        
        # Perform split function
        def perform_split():
            if not ranges_list:
                messagebox.showerror("Error", "Please add at least one page range.")
                return
            
            # Validate all ranges
            validated_ranges = []
            for i, range_item in enumerate(ranges_list):
                try:
                    start = int(range_item["start_entry"].get())
                    end = int(range_item["end_entry"].get())
                    
                    if start < 1 or end < 1:
                        messagebox.showerror("Error", f"Range {i + 1}: Page numbers must be positive.")
                        return
                    if start > total_pages or end > total_pages:
                        messagebox.showerror("Error", f"Range {i + 1}: Page numbers cannot exceed {total_pages}.")
                        return
                    if start > end:
                        messagebox.showerror("Error", f"Range {i + 1}: Start page cannot be greater than end page.")
                        return
                    
                    validated_ranges.append((start, end))
                except ValueError:
                    messagebox.showerror("Error", f"Range {i + 1}: Please enter valid page numbers.")
                    return
            
            # Get output path
            output_path = filedialog.asksaveasfilename(
                title="Save split PDF as",
                defaultextension=".pdf",
                filetypes=get_pdf_filetypes(),
                initialfile=f"split_{os.path.basename(filepath)}",
            )
            
            if not output_path:
                return
            
            try:
                writer = PyPDF2.PdfWriter()
                
                # Add pages from each range in order
                for start, end in validated_ranges:
                    for page_num in range(start - 1, end):  # Convert to 0-indexed
                        writer.add_page(reader.pages[page_num])
                
                with open(output_path, "wb") as output_file:
                    writer.write(output_file)
                
                # Build summary of ranges
                range_summary = ", ".join([f"{s}-{e}" for s, e in validated_ranges])
                total_output_pages = sum(end - start + 1 for start, end in validated_ranges)
                
                split_dialog.destroy()
                messagebox.showinfo(
                    "Success",
                    f"PDF split successfully!\n\n"
                    f"Ranges: {range_summary}\n"
                    f"Total pages in output: {total_output_pages}\n\n"
                    f"Saved to:\n{output_path}",
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to split PDF.\n\n{e}")
        
        def cancel_split():
            split_dialog.destroy()
        
        # Button frame
        btn_frame = tk.Frame(split_dialog, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        
        # Split button
        split_btn = create_primary_button(btn_frame, text="Split & Save", command=perform_split)
        split_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = create_secondary_button(btn_frame, text="Cancel", command=cancel_split)
        cancel_btn.pack(side="left", padx=10)
        
        # Set window size and center
        window_width = 550
        window_height = 450
        center_dialog(split_dialog, window_width, window_height)
        split_dialog.resizable(False, False)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open PDF.\n\n{e}")


def images_to_pdf(app):
    """Convert image files to a PDF."""
    filepaths = filedialog.askopenfilenames(
        title="Select image files (JPG/PNG) to convert",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
        ],
    )
    
    if not filepaths:
        return

    output_path = filedialog.asksaveasfilename(
        title="Save PDF as",
        defaultextension=".pdf",
        filetypes=get_pdf_filetypes(),
    )
    if not output_path:
        return

    try:
        images = []  # images data stored as list elements
        for path in filepaths:
            img = Image.open(path)  # path: directory of the file
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            images.append(img)
        
        # first - first element of the list images
        # Rest - All elements of the list images except first
        first, *rest = images
        first.save(output_path, save_all=True, append_images=rest)

        # Close images to free resources
        for img in images:
            img.close()

        messagebox.showinfo(
            "Success",
            f"Created PDF from {len(filepaths)} image(s):\n{output_path}",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create PDF.\n\n{e}")


def lock_pdf(app):
    """Encrypt a PDF file with a password (AES-256)."""
    filepath = filedialog.askopenfilename(
        title="Select a PDF file to lock",
        filetypes=get_pdf_filetypes(),
    )
    if not filepath:
        return

    # Create password dialog
    lock_dialog = tk.Toplevel(app)
    lock_dialog.title("Lock PDF")
    lock_dialog.configure(bg=BG_COLOR)
    lock_dialog.transient(app)
    lock_dialog.grab_set()

    filename = os.path.basename(filepath)

    # Info
    info_frame = tk.Frame(lock_dialog, bg=BG_COLOR)
    info_frame.pack(pady=(20, 10), padx=30)

    tk.Label(
        info_frame,
        text="🔒 Lock PDF with Password",
        font=(FONT_FAMILY, 13, "bold"),
        bg=BG_COLOR,
        fg="#333333",
    ).pack()

    tk.Label(
        info_frame,
        text=f"File: {filename}",
        font=(FONT_FAMILY, 10),
        bg=BG_COLOR,
        fg="#0078d4",
    ).pack(pady=(8, 0))

    # Password fields
    form_frame = tk.Frame(lock_dialog, bg=BG_COLOR)
    form_frame.pack(pady=15, padx=30)

    show_password = tk.BooleanVar(value=False)

    tk.Label(
        form_frame,
        text="Password:",
        font=(FONT_FAMILY, 10),
        bg=BG_COLOR,
        fg="#333333",
    ).grid(row=0, column=0, sticky="w", pady=5)

    password_entry = tk.Entry(form_frame, font=(FONT_FAMILY, 10), width=25, show="*")
    password_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

    tk.Label(
        form_frame,
        text="Confirm Password:",
        font=(FONT_FAMILY, 10),
        bg=BG_COLOR,
        fg="#333333",
    ).grid(row=1, column=0, sticky="w", pady=5)

    confirm_entry = tk.Entry(form_frame, font=(FONT_FAMILY, 10), width=25, show="*")
    confirm_entry.grid(row=1, column=1, padx=(10, 0), pady=5)

    def toggle_password():
        char = "" if show_password.get() else "*"
        password_entry.config(show=char)
        confirm_entry.config(show=char)

    show_cb = tk.Checkbutton(
        form_frame,
        text="Show Password",
        variable=show_password,
        command=toggle_password,
        font=(FONT_FAMILY, 9),
        bg=BG_COLOR,
        fg="#555555",
        activebackground=BG_COLOR,
    )
    show_cb.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

    def perform_lock():
        password = password_entry.get()
        confirm = confirm_entry.get()

        if not password:
            messagebox.showerror("Error", "Password cannot be empty.", parent=lock_dialog)
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.", parent=lock_dialog)
            return

        output_path = filedialog.asksaveasfilename(
            title="Save locked PDF as",
            defaultextension=".pdf",
            filetypes=get_pdf_filetypes(),
            initialfile=f"locked_{filename}",
        )
        if not output_path:
            return

        try:
            reader = PyPDF2.PdfReader(filepath)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            # Copy metadata if present
            if reader.metadata:
                writer.add_metadata(reader.metadata)

            writer.encrypt(password, use_128bit=True)

            with open(output_path, "wb") as f:
                writer.write(f)

            lock_dialog.destroy()
            messagebox.showinfo(
                "Success",
                f"PDF locked successfully with password!\n\nSaved to:\n{output_path}",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to lock PDF.\n\n{e}", parent=lock_dialog)

    def cancel_lock():
        lock_dialog.destroy()

    # Buttons
    btn_frame = tk.Frame(lock_dialog, bg=BG_COLOR)
    btn_frame.pack(pady=15)

    lock_btn = create_primary_button(btn_frame, text="Lock PDF", command=perform_lock)
    lock_btn.pack(side="left", padx=10)

    cancel_btn = create_secondary_button(btn_frame, text="Cancel", command=cancel_lock)
    cancel_btn.pack(side="left", padx=10)

    # Size and center
    window_width = 420
    window_height = 320
    center_dialog(lock_dialog, window_width, window_height)
    lock_dialog.resizable(False, False)
    password_entry.focus_set()


def unlock_pdf(app):
    """Decrypt a password-protected PDF file."""
    filepath = filedialog.askopenfilename(
        title="Select a password-protected PDF to unlock",
        filetypes=get_pdf_filetypes(),
    )
    if not filepath:
        return

    filename = os.path.basename(filepath)

    # Create password dialog
    unlock_dialog = tk.Toplevel(app)
    unlock_dialog.title("Unlock PDF")
    unlock_dialog.configure(bg=BG_COLOR)
    unlock_dialog.transient(app)
    unlock_dialog.grab_set()

    # Info
    info_frame = tk.Frame(unlock_dialog, bg=BG_COLOR)
    info_frame.pack(pady=(20, 10), padx=30)

    tk.Label(
        info_frame,
        text="🔓 Unlock PDF",
        font=(FONT_FAMILY, 13, "bold"),
        bg=BG_COLOR,
        fg="#333333",
    ).pack()

    tk.Label(
        info_frame,
        text=f"File: {filename}",
        font=(FONT_FAMILY, 10),
        bg=BG_COLOR,
        fg="#0078d4",
    ).pack(pady=(8, 0))

    # Password field
    form_frame = tk.Frame(unlock_dialog, bg=BG_COLOR)
    form_frame.pack(pady=15, padx=30)

    show_password = tk.BooleanVar(value=False)

    tk.Label(
        form_frame,
        text="Password:",
        font=(FONT_FAMILY, 10),
        bg=BG_COLOR,
        fg="#333333",
    ).grid(row=0, column=0, sticky="w", pady=5)

    password_entry = tk.Entry(form_frame, font=(FONT_FAMILY, 10), width=25, show="*")
    password_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

    def toggle_password():
        char = "" if show_password.get() else "*"
        password_entry.config(show=char)

    show_cb = tk.Checkbutton(
        form_frame,
        text="Show Password",
        variable=show_password,
        command=toggle_password,
        font=(FONT_FAMILY, 9),
        bg=BG_COLOR,
        fg="#555555",
        activebackground=BG_COLOR,
    )
    show_cb.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

    def perform_unlock():
        password = password_entry.get()

        if not password:
            messagebox.showerror("Error", "Password cannot be empty.", parent=unlock_dialog)
            return

        try:
            reader = PyPDF2.PdfReader(filepath)

            # Check if the PDF is actually encrypted
            if not reader.is_encrypted:
                messagebox.showinfo(
                    "Info",
                    "This PDF is not password-protected.\nNo unlocking needed.",
                    parent=unlock_dialog,
                )
                return

            # Attempt decryption
            result = reader.decrypt(password)
            if result == 0:
                messagebox.showerror(
                    "Error",
                    "Incorrect password. Please try again.",
                    parent=unlock_dialog,
                )
                return

            output_path = filedialog.asksaveasfilename(
                title="Save unlocked PDF as",
                defaultextension=".pdf",
                filetypes=get_pdf_filetypes(),
                initialfile=f"unlocked_{filename}",
            )
            if not output_path:
                return

            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            # Copy metadata if present
            if reader.metadata:
                writer.add_metadata(reader.metadata)

            with open(output_path, "wb") as f:
                writer.write(f)

            unlock_dialog.destroy()
            messagebox.showinfo(
                "Success",
                f"PDF unlocked successfully!\n\nSaved to:\n{output_path}",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unlock PDF.\n\n{e}", parent=unlock_dialog)

    def cancel_unlock():
        unlock_dialog.destroy()

    # Buttons
    btn_frame = tk.Frame(unlock_dialog, bg=BG_COLOR)
    btn_frame.pack(pady=15)

    unlock_btn = create_primary_button(btn_frame, text="Unlock PDF", command=perform_unlock)
    unlock_btn.pack(side="left", padx=10)

    cancel_btn = create_secondary_button(btn_frame, text="Cancel", command=cancel_unlock)
    cancel_btn.pack(side="left", padx=10)

    # Size and center
    window_width = 420
    window_height = 260
    center_dialog(unlock_dialog, window_width, window_height)
    unlock_dialog.resizable(False, False)
    password_entry.focus_set()
