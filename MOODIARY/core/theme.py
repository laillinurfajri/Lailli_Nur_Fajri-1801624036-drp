# core/theme.py
# ==============================================================================
# MOODIARY DESIGN SYSTEM & THEME ENGINE (PROFESSIONAL DESKTOP UI)
# ==============================================================================
import tkinter as tk
from tkinter import ttk
import core.i18n as language

# ==============================================================================
# COLOR PALETTE (PREMIUM PINK & LIGHT YELLOW)
# ==============================================================================
BG_PINK = "#FCE4EC"               # Primary Soft Pink Background
BG_CARD_YELLOW = "#FFF8E1"        # Primary Cream/Light Yellow Card Surface
BG_WHITE = "#FFFFFF"              # Clean White Surface for Editors & Charts

PRIMARY_YELLOW = "#FFF3B0"        # Primary Action Button Yellow
PRIMARY_YELLOW_HOVER = "#FFE082"  # Primary Yellow Active/Hover

SECONDARY_PINK = "#F8BBD0"        # Secondary Blush Pink Button
SECONDARY_PINK_HOVER = "#F48FB1"  # Secondary Pink Hover

ACCENT_PINK = "#AD1457"           # Deep Pink/Magenta Heading Text
ACCENT_DARK = "#880E4F"           # Dark Magenta Strong Accent
TEXT_DARK = "#4E342E"             # Dark Mocha Body Text
TEXT_MUTED = "#8D6E63"            # Muted Subtitle Text

BORDER_YELLOW = "#FFE082"         # Card Border Yellow
BORDER_PINK = "#F48FB1"           # Border Highlight Pink

# Action Button Colors
BTN_SAVE = "#FFF3B0"
BTN_SAVE_HOVER = "#FFE082"
BTN_UPDATE = "#B3E5FC"
BTN_UPDATE_HOVER = "#81D4FA"
BTN_DELETE = "#FFCDD2"
BTN_DELETE_HOVER = "#EF9A9A"
BTN_CLEAR = "#E1BEE7"
BTN_CLEAR_HOVER = "#CE93D8"
BTN_SUCCESS = "#C8E6C9"
BTN_SUCCESS_HOVER = "#A5D6A7"
BTN_LOGIN = PRIMARY_YELLOW
BTN_REGISTER = SECONDARY_PINK

# ==============================================================================
# TYPOGRAPHY SYSTEM
# ==============================================================================
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_CARD_TITLE = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_ITALIC = ("Segoe UI", 9, "italic")


def center_window(window, width, height):
    window.geometry(f"{width}x{height}")
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def configure_ttk_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        font=FONT_BODY,
        rowheight=30,
        background=BG_CARD_YELLOW,
        fieldbackground=BG_CARD_YELLOW,
        foreground=TEXT_DARK,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=FONT_LABEL,
        background=SECONDARY_PINK,
        foreground=ACCENT_PINK,
        relief="flat",
        padding=6
    )
    style.map(
        "Treeview",
        background=[("selected", "#F48FB1")],
        foreground=[("selected", "#FFFFFF")]
    )

    style.configure(
        "TNotebook",
        background=BG_PINK,
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        font=FONT_LABEL,
        background=PRIMARY_YELLOW,
        foreground=TEXT_DARK,
        padding=[14, 6],
        borderwidth=0
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", SECONDARY_PINK), ("active", PRIMARY_YELLOW_HOVER)],
        foreground=[("selected", ACCENT_DARK)]
    )


def create_header(parent, title, subtitle, bg=BG_PINK):
    header_frame = tk.Frame(parent, bg=bg)
    header_frame.pack(fill="x", padx=20, pady=(15, 8))

    lbl_title = tk.Label(
        header_frame,
        text=title,
        font=FONT_TITLE,
        bg=bg,
        fg=ACCENT_PINK
    )
    lbl_title.pack(anchor="w")

    if subtitle:
        lbl_sub = tk.Label(
            header_frame,
            text=subtitle,
            font=FONT_SUBTITLE,
            bg=bg,
            fg=TEXT_MUTED
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

    return header_frame


def create_card(parent, bg=BG_CARD_YELLOW, border_color=BORDER_YELLOW, pad=12):
    card = tk.Frame(
        parent,
        bg=bg,
        bd=1,
        relief="solid",
        highlightbackground=border_color,
        highlightthickness=1
    )
    return card


def create_back_header(parent, title, subtitle, on_back_callback, bg=BG_PINK):
    header_frame = tk.Frame(parent, bg=bg)
    header_frame.pack(fill="x", padx=20, pady=(12, 8))

    top_bar = tk.Frame(header_frame, bg=bg)
    top_bar.pack(fill="x", pady=(0, 6))

    if on_back_callback:
        btn_back = tk.Button(
            top_bar,
            text=language.get_text("back_to_main"),
            command=on_back_callback,
            bg=SECONDARY_PINK,
            activebackground=SECONDARY_PINK_HOVER,
            fg=ACCENT_DARK,
            font=("Segoe UI", 9, "bold"),
            bd=0,
            cursor="hand2",
            padx=12,
            pady=5
        )
        btn_back.pack(side="left")

    lbl_title = tk.Label(
        header_frame,
        text=title,
        font=FONT_TITLE,
        bg=bg,
        fg=ACCENT_PINK
    )
    lbl_title.pack(anchor="w")

    if subtitle:
        lbl_sub = tk.Label(
            header_frame,
            text=subtitle,
            font=FONT_SUBTITLE,
            bg=bg,
            fg=TEXT_DARK
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

    return header_frame
