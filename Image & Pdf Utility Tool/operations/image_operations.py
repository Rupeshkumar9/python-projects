"""
Image operations for the Image & PDF Utility Tool.
"""
import os
import io
import math
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from utils.helpers import center_dialog, get_image_filetypes, get_save_image_filetypes
from utils.ui_components import create_primary_button, create_secondary_button, BG_COLOR, FONT_FAMILY


def resize_image(app):
    """Upload and resize an image file."""
    # Select an image file
    filepath = filedialog.askopenfilename(
        title="Select an image to resize",
        filetypes=get_image_filetypes(),
    )
    
    if not filepath:
        return
    
    try:
        # Open the image and get original dimensions
        img = Image.open(filepath)
        original_width, original_height = img.size
        
        # Create a dialog window for resize options
        resize_dialog = tk.Toplevel(app)
        resize_dialog.title("Resize Image")
        resize_dialog.configure(bg=BG_COLOR)
        resize_dialog.geometry("400x350")
        resize_dialog.resizable(False, False)
        resize_dialog.transient(app)
        resize_dialog.grab_set()
        
        # Center the dialog
        center_dialog(resize_dialog, 400, 350)
        
        # Display original dimensions
        info_label = tk.Label(
            resize_dialog,
            text=f"Original Size: {original_width} x {original_height} pixels",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
            fg="#333333",
        )
        info_label.pack(pady=(20, 15))
        
        # Filename display
        filename = os.path.basename(filepath)
        file_label = tk.Label(
            resize_dialog,
            text=f"File: {filename}",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#555555",
        )
        file_label.pack(pady=(0, 20))
        
        # Width input
        width_frame = tk.Frame(resize_dialog, bg=BG_COLOR)
        width_frame.pack(pady=5)
        tk.Label(
            width_frame,
            text="New Width:",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            width=12,
            anchor="e",
        ).pack(side="left", padx=(0, 10))
        width_entry = tk.Entry(width_frame, font=(FONT_FAMILY, 10), width=15)
        width_entry.insert(0, str(original_width))
        width_entry.pack(side="left")
        tk.Label(width_frame, text="px", font=(FONT_FAMILY, 10), bg=BG_COLOR).pack(side="left", padx=5)
        
        # Height input
        height_frame = tk.Frame(resize_dialog, bg=BG_COLOR)
        height_frame.pack(pady=5)
        tk.Label(
            height_frame,
            text="New Height:",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            width=12,
            anchor="e",
        ).pack(side="left", padx=(0, 10))
        height_entry = tk.Entry(height_frame, font=(FONT_FAMILY, 10), width=15)
        height_entry.insert(0, str(original_height))
        height_entry.pack(side="left")
        tk.Label(height_frame, text="px", font=(FONT_FAMILY, 10), bg=BG_COLOR).pack(side="left", padx=5)
        
        # Maintain aspect ratio checkbox
        maintain_ratio = tk.BooleanVar(value=True)
        ratio_check = tk.Checkbutton(
            resize_dialog,
            text="Maintain aspect ratio",
            variable=maintain_ratio,
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            activebackground=BG_COLOR,
        )
        ratio_check.pack(pady=15)
        
        # Function to update height when width changes (if maintain ratio is on)
        def on_width_change(*args):
            if maintain_ratio.get():
                try:
                    new_width = int(width_entry.get())
                    new_height = int(new_width * original_height / original_width)
                    height_entry.delete(0, tk.END)
                    height_entry.insert(0, str(new_height))
                except ValueError:
                    pass
        
        # Function to update width when height changes (if maintain ratio is on)
        def on_height_change(*args):
            if maintain_ratio.get():
                try:
                    new_height = int(height_entry.get())
                    new_width = int(new_height * original_width / original_height)
                    width_entry.delete(0, tk.END)
                    width_entry.insert(0, str(new_width))
                except ValueError:
                    pass
        
        # Bind focus out events
        width_entry.bind("<FocusOut>", on_width_change)
        height_entry.bind("<FocusOut>", on_height_change)
        
        # Function to perform the resize
        def perform_resize():
            try:
                new_width = int(width_entry.get())
                new_height = int(height_entry.get())
                
                if new_width <= 0 or new_height <= 0:
                    messagebox.showerror("Error", "Width and height must be positive numbers.")
                    return
                
                # Get output path
                file_ext = os.path.splitext(filepath)[1].lower()
                output_path = filedialog.asksaveasfilename(
                    title="Save resized image as",
                    defaultextension=file_ext,
                    filetypes=get_save_image_filetypes(),
                    initialfile=f"resized_{os.path.basename(filepath)}",
                )
                
                if not output_path:
                    return
                
                # Resize the image using high-quality resampling
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert if needed for JPEG
                if output_path.lower().endswith(('.jpg', '.jpeg')) and resized_img.mode in ('RGBA', 'P'):
                    resized_img = resized_img.convert('RGB')
                
                resized_img.save(output_path)
                resized_img.close()
                img.close()
                
                resize_dialog.destroy()
                messagebox.showinfo(
                    "Success",
                    f"Image resized successfully!\n\nOriginal: {original_width} x {original_height}\nNew: {new_width} x {new_height}\n\nSaved to:\n{output_path}",
                )
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for width and height.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to resize image.\n\n{e}")
        
        # UI for resize dialog
        btn_frame = tk.Frame(resize_dialog, bg=BG_COLOR)  # Button frame
        btn_frame.pack(pady=20)
        
        # Resize button
        resize_btn = create_primary_button(btn_frame, text="Resize & Save", command=perform_resize)
        resize_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = create_secondary_button(
            btn_frame, 
            text="Cancel", 
            command=lambda: [img.close(), resize_dialog.destroy()]
        )
        cancel_btn.pack(side="left", padx=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image.\n\n{e}")


def crop_image(app):
    """Upload and crop an image file."""
    # Select an image file
    filepath = filedialog.askopenfilename(
        title="Select an image to crop",
        filetypes=get_image_filetypes(),
    )
    
    if not filepath:
        return
    
    try:
        # Open the image
        original_img = Image.open(filepath)
        original_width, original_height = original_img.size
        
        # Create crop dialog window
        crop_dialog = tk.Toplevel(app)
        crop_dialog.title("Crop Image")
        crop_dialog.configure(bg=BG_COLOR)
        crop_dialog.transient(app)
        crop_dialog.grab_set()
        
        # Calculate display size (fit within 800x600 while maintaining aspect ratio)
        max_display_width = 800
        max_display_height = 600
        
        scale = min(max_display_width / original_width, max_display_height / original_height, 1.0)
        display_width = int(original_width * scale)
        display_height = int(original_height * scale)
        
        # Resize image for display
        display_img = original_img.resize((display_width, display_height), Image.Resampling.LANCZOS)
        photo_img = ImageTk.PhotoImage(display_img)
        
        # Handle size and colors
        HANDLE_SIZE = 10
        HANDLE_COLOR = "#0078d4"
        BORDER_COLOR = "#0078d4"
        OVERLAY_COLOR = "#000000"
        OVERLAY_ALPHA = 0.5
        
        # Crop state - initialized to full image
        crop_state = {
            "x1": 0,
            "y1": 0,
            "x2": display_width,
            "y2": display_height,
            "dragging": None,  # Which handle/edge is being dragged
            "drag_start_x": 0,
            "drag_start_y": 0,
            "scale": scale,
        }
        
        # Info frame at the top
        info_frame = tk.Frame(crop_dialog, bg=BG_COLOR)
        info_frame.pack(pady=10, fill="x")
        
        filename = os.path.basename(filepath)
        file_label = tk.Label(
            info_frame,
            text=f"File: {filename} | Original: {original_width} x {original_height} px",
            font=(FONT_FAMILY, 10, "bold"),
            bg=BG_COLOR,
            fg="#333333",
        )
        file_label.pack()
        
        instruction_label = tk.Label(
            info_frame,
            text="Drag the handles or edges to adjust the crop area",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#555555",
        )
        instruction_label.pack(pady=(5, 0))
        
        # Selection info label
        selection_label = tk.Label(
            info_frame,
            text=f"Crop Size: {original_width} x {original_height} px",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#0078d4",
        )
        selection_label.pack(pady=(5, 0))
        
        # Canvas frame
        canvas_frame = tk.Frame(crop_dialog, bg="#333333", padx=2, pady=2)
        canvas_frame.pack(padx=20, pady=10)
        
        # Create canvas with the image
        canvas = tk.Canvas(
            canvas_frame,
            width=display_width,
            height=display_height,
            bg="white",
            highlightthickness=0,
        )
        canvas.pack()
        
        # Display the image on canvas
        canvas.create_image(0, 0, anchor="nw", image=photo_img, tags="image")
        canvas.image = photo_img  # Keep reference
        
        def update_overlay():
            """Update the dark overlay and crop handles"""
            canvas.delete("overlay")
            canvas.delete("handles")
            canvas.delete("border")
            
            x1, y1 = crop_state["x1"], crop_state["y1"]
            x2, y2 = crop_state["x2"], crop_state["y2"]
            
            # Create semi-transparent overlay for non-selected areas
            # Top overlay
            if y1 > 0:
                canvas.create_rectangle(0, 0, display_width, y1, 
                    fill=OVERLAY_COLOR, stipple="gray50", tags="overlay")
            # Bottom overlay
            if y2 < display_height:
                canvas.create_rectangle(0, y2, display_width, display_height, 
                    fill=OVERLAY_COLOR, stipple="gray50", tags="overlay")
            # Left overlay
            if x1 > 0:
                canvas.create_rectangle(0, y1, x1, y2, 
                    fill=OVERLAY_COLOR, stipple="gray50", tags="overlay")
            # Right overlay
            if x2 < display_width:
                canvas.create_rectangle(x2, y1, display_width, y2, 
                    fill=OVERLAY_COLOR, stipple="gray50", tags="overlay")
            
            # Draw crop border
            canvas.create_rectangle(x1, y1, x2, y2, 
                outline=BORDER_COLOR, width=2, tags="border")
            
            # Draw handles at corners and edges
            hs = HANDLE_SIZE // 2
            
            # Corner handles
            handles = {
                "nw": (x1, y1),
                "ne": (x2, y1),
                "sw": (x1, y2),
                "se": (x2, y2),
            }
            
            # Edge handles (midpoints)
            handles.update({
                "n": ((x1 + x2) // 2, y1),
                "s": ((x1 + x2) // 2, y2),
                "w": (x1, (y1 + y2) // 2),
                "e": (x2, (y1 + y2) // 2),
            })
            
            for handle_id, (hx, hy) in handles.items():
                canvas.create_rectangle(
                    hx - hs, hy - hs, hx + hs, hy + hs,
                    fill=HANDLE_COLOR, outline="white", width=1,
                    tags=("handles", f"handle_{handle_id}")
                )
            
            # Update selection label
            crop_w = int((x2 - x1) / scale)
            crop_h = int((y2 - y1) / scale)
            selection_label.config(text=f"Crop Size: {crop_w} x {crop_h} px")
        
        def get_handle_at(x, y):
            """Determine which handle or edge is at the given coordinates"""
            x1, y1 = crop_state["x1"], crop_state["y1"]
            x2, y2 = crop_state["x2"], crop_state["y2"]
            hs = HANDLE_SIZE
            
            # Check corners first (higher priority)
            if abs(x - x1) <= hs and abs(y - y1) <= hs:
                return "nw"
            if abs(x - x2) <= hs and abs(y - y1) <= hs:
                return "ne"
            if abs(x - x1) <= hs and abs(y - y2) <= hs:
                return "sw"
            if abs(x - x2) <= hs and abs(y - y2) <= hs:
                return "se"
            
            # Check edge midpoints
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            if abs(x - mid_x) <= hs and abs(y - y1) <= hs:
                return "n"
            if abs(x - mid_x) <= hs and abs(y - y2) <= hs:
                return "s"
            if abs(x - x1) <= hs and abs(y - mid_y) <= hs:
                return "w"
            if abs(x - x2) <= hs and abs(y - mid_y) <= hs:
                return "e"
            
            # Check if on edges (for edge dragging)
            edge_tolerance = 8
            if x1 - edge_tolerance <= x <= x2 + edge_tolerance:
                if abs(y - y1) <= edge_tolerance:
                    return "n"
                if abs(y - y2) <= edge_tolerance:
                    return "s"
            if y1 - edge_tolerance <= y <= y2 + edge_tolerance:
                if abs(x - x1) <= edge_tolerance:
                    return "w"
                if abs(x - x2) <= edge_tolerance:
                    return "e"
            
            # Check if inside crop area (for moving entire selection)
            if x1 < x < x2 and y1 < y < y2:
                return "move"
            
            return None
        
        def update_cursor(event):
            """Update cursor based on hover position"""
            handle = get_handle_at(event.x, event.y)
            cursors = {
                "nw": "top_left_corner",
                "ne": "top_right_corner",
                "sw": "bottom_left_corner",
                "se": "bottom_right_corner",
                "n": "sb_v_double_arrow",
                "s": "sb_v_double_arrow",
                "w": "sb_h_double_arrow",
                "e": "sb_h_double_arrow",
                "move": "fleur",
            }
            canvas.config(cursor=cursors.get(handle, "arrow"))
        
        def on_mouse_press(event):
            """Handle mouse button press"""
            handle = get_handle_at(event.x, event.y)
            if handle:
                crop_state["dragging"] = handle
                crop_state["drag_start_x"] = event.x
                crop_state["drag_start_y"] = event.y
                crop_state["orig_x1"] = crop_state["x1"]
                crop_state["orig_y1"] = crop_state["y1"]
                crop_state["orig_x2"] = crop_state["x2"]
                crop_state["orig_y2"] = crop_state["y2"]
        
        def on_mouse_drag(event):
            """Handle mouse drag"""
            if not crop_state["dragging"]:
                return
            
            dx = event.x - crop_state["drag_start_x"]
            dy = event.y - crop_state["drag_start_y"]
            handle = crop_state["dragging"]
            
            min_size = 20  # Minimum crop size
            
            # Calculate new positions based on which handle is being dragged
            new_x1, new_y1 = crop_state["orig_x1"], crop_state["orig_y1"]
            new_x2, new_y2 = crop_state["orig_x2"], crop_state["orig_y2"]
            
            if handle == "move":
                # Move entire selection
                new_x1 = max(0, min(crop_state["orig_x1"] + dx, display_width - (new_x2 - new_x1)))
                new_y1 = max(0, min(crop_state["orig_y1"] + dy, display_height - (new_y2 - new_y1)))
                width = crop_state["orig_x2"] - crop_state["orig_x1"]
                height = crop_state["orig_y2"] - crop_state["orig_y1"]
                new_x2 = new_x1 + width
                new_y2 = new_y1 + height
            else:
                # Handle edge/corner dragging
                if "w" in handle:
                    new_x1 = max(0, min(crop_state["orig_x1"] + dx, new_x2 - min_size))
                if "e" in handle:
                    new_x2 = max(new_x1 + min_size, min(crop_state["orig_x2"] + dx, display_width))
                if "n" in handle:
                    new_y1 = max(0, min(crop_state["orig_y1"] + dy, new_y2 - min_size))
                if "s" in handle:
                    new_y2 = max(new_y1 + min_size, min(crop_state["orig_y2"] + dy, display_height))
            
            crop_state["x1"] = new_x1
            crop_state["y1"] = new_y1
            crop_state["x2"] = new_x2
            crop_state["y2"] = new_y2
            
            update_overlay()
        
        def on_mouse_release(event):
            """Handle mouse release"""
            crop_state["dragging"] = None
        
        # Bind mouse events
        canvas.bind("<Motion>", update_cursor)
        canvas.bind("<ButtonPress-1>", on_mouse_press)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_release)
        
        def reset_selection():
            """Reset crop to full image"""
            crop_state["x1"] = 0
            crop_state["y1"] = 0
            crop_state["x2"] = display_width
            crop_state["y2"] = display_height
            update_overlay()
        
        def perform_crop():
            """Crop and save the image"""
            x1, y1 = crop_state["x1"], crop_state["y1"]
            x2, y2 = crop_state["x2"], crop_state["y2"]
            
            # Convert to original image coordinates
            orig_x1 = int(x1 / scale)
            orig_y1 = int(y1 / scale)
            orig_x2 = int(x2 / scale)
            orig_y2 = int(y2 / scale)
            
            # Clamp to image bounds
            orig_x1 = max(0, min(orig_x1, original_width))
            orig_y1 = max(0, min(orig_y1, original_height))
            orig_x2 = max(0, min(orig_x2, original_width))
            orig_y2 = max(0, min(orig_y2, original_height))
            
            # Get output path
            file_ext = os.path.splitext(filepath)[1].lower()
            output_path = filedialog.asksaveasfilename(
                title="Save cropped image as",
                defaultextension=file_ext,
                filetypes=get_save_image_filetypes(),
                initialfile=f"cropped_{os.path.basename(filepath)}",
            )
            
            if not output_path:
                return
            
            try:
                cropped_img = original_img.crop((orig_x1, orig_y1, orig_x2, orig_y2))
                
                if output_path.lower().endswith(('.jpg', '.jpeg')) and cropped_img.mode in ('RGBA', 'P'):
                    cropped_img = cropped_img.convert('RGB')
                
                cropped_img.save(output_path)
                cropped_img.close()
                original_img.close()
                display_img.close()
                
                crop_width = orig_x2 - orig_x1
                crop_height = orig_y2 - orig_y1
                
                crop_dialog.destroy()
                messagebox.showinfo(
                    "Success",
                    f"Image cropped successfully!\n\nOriginal: {original_width} x {original_height}\nCropped: {crop_width} x {crop_height}\n\nSaved to:\n{output_path}",
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save cropped image.\n\n{e}")
        
        def cancel_crop():
            """Close dialog without saving"""
            original_img.close()
            display_img.close()
            crop_dialog.destroy()
        
        # Button frame
        btn_frame = tk.Frame(crop_dialog, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        
        # Reset button
        reset_btn = tk.Button(
            btn_frame,
            text="Reset",
            command=reset_selection,
            font=(FONT_FAMILY, 11),
            bg="#e0e0e0",
            fg="#333333",
            activebackground="#c0c0c0",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
        )
        reset_btn.pack(side="left", padx=10)
        
        # Crop & Save button
        crop_btn = create_primary_button(btn_frame, text="Crop & Save", command=perform_crop)
        crop_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=cancel_crop,
            font=(FONT_FAMILY, 11),
            bg="#e0e0e0",
            fg="#333333",
            activebackground="#c0c0c0",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Initialize overlay and handles
        update_overlay()
        
        # Set window size
        window_width = max(display_width + 60, 500)
        window_height = display_height + 180
        center_dialog(crop_dialog, window_width, window_height)
        crop_dialog.resizable(False, False)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image.\n\n{e}")


def compress_image(app):
    """Upload and compress an image file to a target size."""
    # Select an image file
    filepath = filedialog.askopenfilename(
        title="Select an image to compress",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
        ],
    )
    
    if not filepath:
        return
    
    try:
        # Open the image and get file info
        img = Image.open(filepath)
        original_width, original_height = img.size
        original_size_bytes = os.path.getsize(filepath)
        original_size_kb = original_size_bytes / 1024
        
        # Create a dialog window for compression options
        compress_dialog = tk.Toplevel(app)
        compress_dialog.title("Compress Image")
        compress_dialog.configure(bg=BG_COLOR)
        compress_dialog.geometry("450x400")
        compress_dialog.resizable(False, False)
        compress_dialog.transient(app)
        compress_dialog.grab_set()
        
        # Center the dialog
        center_dialog(compress_dialog, 450, 400)
        
        # Title
        title_label = tk.Label(
            compress_dialog,
            text="Image Compression",
            font=(FONT_FAMILY, 14, "bold"),
            bg=BG_COLOR,
            fg="#333333",
        )
        title_label.pack(pady=(20, 10))
        
        # Filename display
        filename = os.path.basename(filepath)
        file_label = tk.Label(
            compress_dialog,
            text=f"File: {filename}",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#555555",
        )
        file_label.pack(pady=(0, 5))
        
        # Display original image info
        info_frame = tk.Frame(compress_dialog, bg="#e8e8e8", padx=15, pady=10)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            info_frame,
            text=f"Dimensions: {original_width} x {original_height} pixels",
            font=(FONT_FAMILY, 10),
            bg="#e8e8e8",
            fg="#333333",
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=f"Current Size: {original_size_kb:.2f} KB ({original_size_bytes:,} bytes)",
            font=(FONT_FAMILY, 10, "bold"),
            bg="#e8e8e8",
            fg="#0078d4",
        ).pack(anchor="w", pady=(5, 0))
        
        # Target size input
        target_frame = tk.Frame(compress_dialog, bg=BG_COLOR)
        target_frame.pack(pady=20)
        
        tk.Label(
            target_frame,
            text="Target Size:",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
            anchor="e",
        ).pack(side="left", padx=(0, 10))
        
        target_entry = tk.Entry(target_frame, font=(FONT_FAMILY, 11), width=10)
        # Default to 50% of original size, minimum 10 KB
        default_target = max(10, int(original_size_kb * 0.5))
        target_entry.insert(0, str(default_target))
        target_entry.pack(side="left")
        
        tk.Label(
            target_frame,
            text="KB",
            font=(FONT_FAMILY, 11, "bold"),
            bg=BG_COLOR,
        ).pack(side="left", padx=5)
        
        # Info label
        info_label = tk.Label(
            compress_dialog,
            text="Image will be resized proportionally to achieve target size\nwithout losing image quality.",
            font=(FONT_FAMILY, 9),
            bg=BG_COLOR,
            fg="#666666",
        )
        info_label.pack(pady=5)
        
        # Status label
        status_label = tk.Label(
            compress_dialog,
            text="",
            font=(FONT_FAMILY, 10),
            bg=BG_COLOR,
            fg="#0078d4",
        )
        status_label.pack(pady=5)
        
        # Function to compress image to target size using smart resizing
        def compress_to_target_size(image, target_kb, output_path):
            """Compress image to target size by proportional resizing."""
            target_bytes = target_kb * 1024
            
            # Convert image to RGB if needed (for JPEG output)
            working_img = image.copy()
            if working_img.mode in ('RGBA', 'P'):
                working_img = working_img.convert('RGB')
            
            current_width, current_height = working_img.size
            
            # First, check current size at high quality (85)
            buffer = io.BytesIO()
            working_img.save(buffer, format='JPEG', quality=85, optimize=True)
            current_size = buffer.tell()
            
            # If already under target, save with high quality
            if current_size <= target_bytes:
                working_img.save(output_path, format='JPEG', quality=85, optimize=True)
                return os.path.getsize(output_path), current_width, current_height
            
            # Calculate scale factor based on file size ratio
            # File size roughly proportional to number of pixels
            size_ratio = target_bytes / current_size
            # Use square root because file size is proportional to area (width * height)
            scale_factor = math.sqrt(size_ratio) * 0.95  # 5% margin for safety
            
            # Apply scaling iteratively to reach target size
            best_img = None
            best_size = current_size
            
            for attempt in range(10):
                # Calculate new dimensions
                new_width = max(50, int(current_width * scale_factor))
                new_height = max(50, int(current_height * scale_factor))
                
                # Resize with high-quality LANCZOS resampling
                resized = working_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Check size at quality 85 (good balance of quality and size)
                buffer = io.BytesIO()
                resized.save(buffer, format='JPEG', quality=85, optimize=True)
                new_size = buffer.tell()
                
                if new_size <= target_bytes:
                    best_img = resized
                    best_size = new_size
                    
                    # Try to get a bit larger while still under target
                    scale_factor *= 1.05
                else:
                    # Need to reduce more
                    scale_factor *= 0.9
                
                # Stop if we're close enough (within 5% of target)
                if best_img is not None and best_size >= target_bytes * 0.90:
                    break
                
                # Prevent too small images
                if new_width <= 50 or new_height <= 50:
                    if best_img is None:
                        best_img = resized
                        best_size = new_size
                    break
            
            # If we still don't have a valid image, use the smallest we got
            if best_img is None:
                # Last resort: reduce to minimum size
                min_width = max(50, int(current_width * 0.1))
                min_height = max(50, int(current_height * 0.1))
                best_img = working_img.resize((min_width, min_height), Image.Resampling.LANCZOS)
            
            # Save the result
            best_img.save(output_path, format='JPEG', quality=85, optimize=True)
            final_size = os.path.getsize(output_path)
            final_width, final_height = best_img.size
            
            working_img.close()
            best_img.close()
            
            return final_size, final_width, final_height
        
        # Function to perform the compression
        def perform_compress():
            try:
                target_kb = int(target_entry.get())
                if target_kb <= 0:
                    messagebox.showerror("Error", "Target size must be a positive number.")
                    return
                
                # Get output path
                output_path = filedialog.asksaveasfilename(
                    title="Save compressed image as",
                    defaultextension=".jpg",
                    filetypes=[
                        ("JPEG files", "*.jpg *.jpeg"),
                    ],
                    initialfile=f"compressed_{os.path.splitext(filename)[0]}.jpg",
                )
                
                if not output_path:
                    return
                
                status_label.config(text="Compressing... Please wait.", fg="#0078d4")
                compress_dialog.update()
                
                final_size, final_width, final_height = compress_to_target_size(img, target_kb, output_path)
                final_size_kb = final_size / 1024
                
                img.close()
                compress_dialog.destroy()
                
                reduction = ((original_size_bytes - final_size) / original_size_bytes) * 100
                messagebox.showinfo(
                    "Success",
                    f"Image compressed successfully!\n\n"
                    f"Original: {original_size_kb:.2f} KB ({original_width} x {original_height})\n"
                    f"Compressed: {final_size_kb:.2f} KB ({final_width} x {final_height})\n"
                    f"Reduction: {reduction:.1f}%\n\n"
                    f"Saved to:\n{output_path}",
                )
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric value for target size.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to compress image.\n\n{e}")
        
        # Buttons
        btn_frame = tk.Frame(compress_dialog, bg=BG_COLOR)
        btn_frame.pack(pady=20)
        
        # Compress button
        compress_btn = create_primary_button(btn_frame, text="Compress & Save", command=perform_compress)
        compress_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = create_secondary_button(
            btn_frame,
            text="Cancel",
            command=lambda: [img.close(), compress_dialog.destroy()]
        )
        cancel_btn.pack(side="left", padx=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image.\n\n{e}")
