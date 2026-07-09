# manager/quote.py
# ==============================================================================
# MOODIARY - DAILY INSPIRATIONAL QUOTE (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import tkinter as tk
import random
import core.i18n as language


from core.theme import (
    BG_PINK, BG_CARD_YELLOW,
    PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER,
    SECONDARY_PINK,
    ACCENT_PINK, ACCENT_DARK,
    TEXT_DARK, TEXT_MUTED,
    BORDER_YELLOW,
    FONT_TITLE, FONT_SUBTITLE, FONT_ITALIC,
    center_window, create_back_header
)




def render_quote(parent_container, on_back_callback=None):
    """
    Merender halaman Daily Quote di dalam parent_container (Single-Window).
    """
    current_lang = language.LANG


    title_text = "💬 Daily Inspirational Quote"
    desc_text = (
        "A motivational quote to start your positive journey today ✨"
        if current_lang == "EN"
        else "Satu kutipan penyemangat untuk mengawali langkah positifmu hari ini ✨"
    )


    create_back_header(
        parent_container,
        title_text,
        desc_text,
        on_back_callback
    )


    content_area = tk.Frame(parent_container, bg=BG_PINK)
    content_area.pack(fill="both", expand=True, padx=80, pady=24)


    card = tk.Frame(
        content_area,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        highlightbackground=BORDER_YELLOW,
        highlightthickness=1
    )
    card.pack(fill="both", expand=True, pady=16)


    lbl_quote = tk.Label(
        card,
        text="",
        font=("Segoe UI", 16, "italic"),
        bg=BG_CARD_YELLOW,
        fg=ACCENT_DARK,
        wraplength=650,
        justify="center",
        pady=40
    )
    lbl_quote.pack(expand=True)


    def ganti_quote():
        lang_code = language.LANG
        daftar = language.QUOTES[lang_code]
        q = random.choice(daftar)
        lbl_quote.config(text=f'"{q}"')


    btn_frame = tk.Frame(content_area, bg=BG_PINK)
    btn_frame.pack(fill="x", pady=(8, 20))


    btn_text = (
        "✨ Read Another Inspirational Quote"
        if current_lang == "EN"
        else "✨ Baca Kutipan Inspiratif Lainnya"
    )


    tk.Button(
        btn_frame,
        text=btn_text,
        command=ganti_quote,
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 11, "bold"),
        fg=TEXT_DARK,
        bd=0,
        cursor="hand2",
        pady=10
    ).pack(fill="x")


    ganti_quote()




def klik_quote(parent_container=None, on_back_callback=None):
    if parent_container:
        render_quote(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("💬 Daily Inspirational Quote - Moodiary")
        window.configure(bg=BG_PINK)
        center_window(window, 580, 380)
        render_quote(window, None)
