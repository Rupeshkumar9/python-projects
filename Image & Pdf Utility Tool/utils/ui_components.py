"""
Reusable UI components for the Image & PDF Utility Tool.
"""
import tkinter as tk


# Style constants
FONT_FAMILY = "Segoe UI"
PRIMARY_BG = "#0078d4"
PRIMARY_ACTIVE_BG = "#005a9e"
SECONDARY_BG = "#e0e0e0"
SECONDARY_ACTIVE_BG = "#c0c0c0"
BG_COLOR = "#f5f5f5"


def create_primary_button(parent, text, command):
    """Create a styled primary action button (blue)."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT_FAMILY, 11, "bold"),
        bg=PRIMARY_BG,
        fg="white",
        activebackground=PRIMARY_ACTIVE_BG,
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
    )
    return btn


def create_secondary_button(parent, text, command):
    """Create a styled secondary/cancel button (gray)."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT_FAMILY, 11),
        bg=SECONDARY_BG,
        fg="#333333",
        activebackground=SECONDARY_ACTIVE_BG,
        activeforeground="#333333",
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
    )
    return btn


def create_title_label(parent, text):
    """Create a title label."""
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, 20, "bold"),
        bg=BG_COLOR,
        fg="#333333",
    )


def create_subtitle_label(parent, text):
    """Create a subtitle label."""
    return tk.Label(
        parent,
        text=text,
        font=(FONT_FAMILY, 11),
        bg=BG_COLOR,
        fg="#555555",
    )


def create_info_label(parent, text, bold=False, fg_color="#333333"):
    """Create an info label with customizable style."""
    font_style = (FONT_FAMILY, 10, "bold") if bold else (FONT_FAMILY, 10)
    return tk.Label(
        parent,
        text=text,
        font=font_style,
        bg=BG_COLOR,
        fg=fg_color,
    )
