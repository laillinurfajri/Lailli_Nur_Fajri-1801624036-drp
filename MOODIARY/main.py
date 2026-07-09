# main.py
# ==============================================================================
# MOODIARY - PROFESSIONAL SINGLE-WINDOW DESKTOP APPLICATION
# ==============================================================================
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
from datetime import datetime

import core.database as database
import core.i18n as language
from core.i18n import get_text, set_language, QUOTES

from core.theme import (
    BG_PINK, BG_CARD_YELLOW, BG_WHITE,
    PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER,
    SECONDARY_PINK,
    ACCENT_PINK, ACCENT_DARK,
    TEXT_DARK, TEXT_MUTED,
    BORDER_YELLOW,
    BTN_LOGIN, BTN_REGISTER,
    FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY, FONT_SMALL, FONT_ITALIC,
    center_window, configure_ttk_styles
)

# Render functions untuk Single-Window frame navigation
from views.daily_journal_view import render_daily_journal
from views.mood_tracker_view import render_mood_tracker
from views.todo_list_view import render_todo_list
from views.wish_list_view import render_wish_list
from views.quotes_view import render_quote
from views.analytics_view import render_statistik
from views.settings_view import render_settings
from views.register_view import render_register

# Setup database sistem
database.init_db()

# ==============================================================================
# ROOT APPLICATION WINDOW (SINGLE WINDOW HOST)
# ==============================================================================
app = tk.Tk()
app.title("🌸 Moodiary - Personal Digital Journal & Task Manager")
app.configure(bg=BG_PINK)
app.minsize(1020, 680)
center_window(app, 1080, 740)
configure_ttk_styles()

current_user = ""

# 3 Frame Utama di Root Window
login_frame = tk.Frame(app, bg=BG_PINK)
main_frame = tk.Frame(app, bg=BG_PINK)
feature_container = tk.Frame(app, bg=BG_PINK)

# ==============================================================================
# GLOBAL FOOTER CREDIT BAR ("BY DJL")
# ==============================================================================
global_footer = tk.Frame(app, bg=BG_PINK)
global_footer.pack(side="bottom", fill="x", pady=(2, 6))

tk.Label(
    global_footer,
    text="✦ Moodiary — Personal Digital Journal & Task Assistant  •  Crafted with Love by DJL ✦",
    font=FONT_ITALIC,
    bg=BG_PINK,
    fg=ACCENT_PINK
).pack()


# ==============================================================================
# ROUTING & SINGLE-WINDOW FRAME SWITCHER
# ==============================================================================
def tampilkan_login():
    main_frame.pack_forget()
    feature_container.pack_forget()
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    login_frame.pack(side="top", fill="both", expand=True)


def tampilkan_main_menu():
    login_frame.pack_forget()
    feature_container.pack_forget()
    refresh_semua_teks()
    main_frame.pack(side="top", fill="both", expand=True)


def tampilkan_fitur(render_func, *args, **kwargs):
    """
    Mengganti tampilan utama ke menu fitur yang dipilih di jendela yang sama.
    Menyertakan tombol '◀ Kembali ke Menu Utama' pada header fitur.
    """
    login_frame.pack_forget()
    main_frame.pack_forget()

    for w in feature_container.winfo_children():
        w.destroy()

    render_func(feature_container, *args, on_back_callback=tampilkan_main_menu, **kwargs)
    feature_container.pack(side="top", fill="both", expand=True)


def tampilkan_register_page():
    """
    Menampilkan halaman register di jendela yang sama dengan tombol kembali ke Login.
    """
    login_frame.pack_forget()
    main_frame.pack_forget()

    for w in feature_container.winfo_children():
        w.destroy()

    render_register(feature_container, on_back_callback=tampilkan_login)
    feature_container.pack(fill="both", expand=True)


# ==============================================================================
# 1. LOGIN SCREEN (LOGIN FRAME)
# ==============================================================================
login_card_wrapper = tk.Frame(login_frame, bg=BG_PINK)
login_card_wrapper.pack(expand=True)

login_card = tk.Frame(
    login_card_wrapper,
    bg=BG_CARD_YELLOW,
    bd=1,
    relief="solid",
    highlightbackground=BORDER_YELLOW,
    highlightthickness=1
)
login_card.pack(padx=20, pady=20)

tk.Label(
    login_card,
    text="🌸 MOODIARY 🌸",
    font=("Segoe UI", 26, "bold"),
    bg=BG_CARD_YELLOW,
    fg=ACCENT_PINK
).pack(pady=(28, 6), padx=50)

lbl_sub = tk.Label(
    login_card,
    text="Personal Digital Journal & Task Assistant",
    font=FONT_SUBTITLE,
    bg=BG_CARD_YELLOW,
    fg=TEXT_DARK
)
lbl_sub.pack(pady=(0, 24))

form_inner = tk.Frame(login_card, bg=BG_CARD_YELLOW)
form_inner.pack(fill="x", padx=40)

tk.Label(
    form_inner,
    text="👤 Username",
    font=FONT_CARD_TITLE,
    bg=BG_CARD_YELLOW,
    fg=TEXT_DARK
).pack(anchor="w", pady=(0, 4))

entry_username = tk.Entry(
    form_inner,
    font=("Segoe UI", 11),
    bg=BG_WHITE,
    relief="solid",
    bd=1
)
entry_username.pack(fill="x", ipady=5, pady=(0, 14))

tk.Label(
    form_inner,
    text="🔒 Password",
    font=FONT_CARD_TITLE,
    bg=BG_CARD_YELLOW,
    fg=TEXT_DARK
).pack(anchor="w", pady=(0, 4))

entry_password = tk.Entry(
    form_inner,
    show="*",
    font=("Segoe UI", 11),
    bg=BG_WHITE,
    relief="solid",
    bd=1
)
entry_password.pack(fill="x", ipady=5, pady=(0, 24))


def proses_login():
    global current_user
    u = entry_username.get().strip()
    p = entry_password.get().strip()

    if u == "" or p == "":
        messagebox.showwarning("Peringatan", "Harap isi username dan password.")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    result = cursor.fetchone()
    conn.close()

    if result:
        current_user = u
        database.set_active_user(u)
        tampilkan_main_menu()
    else:
        messagebox.showerror("Gagal Masuk", "Username atau Password salah.")


entry_password.bind("<Return>", lambda e: proses_login())

tk.Button(
    form_inner,
    text="🧈 Masuk ke Dasbor",
    command=proses_login,
    bg=BTN_LOGIN,
    activebackground=PRIMARY_YELLOW_HOVER,
    font=("Segoe UI", 11, "bold"),
    fg=TEXT_DARK,
    bd=0,
    cursor="hand2",
    pady=10
).pack(fill="x", pady=(0, 10))

tk.Button(
    form_inner,
    text="🎀 Daftar Akun Baru",
    command=tampilkan_register_page,
    bg=BTN_REGISTER,
    activebackground="#F48FB1",
    font=("Segoe UI", 11, "bold"),
    fg=ACCENT_DARK,
    bd=0,
    cursor="hand2",
    pady=10
).pack(fill="x", pady=(0, 24))

# Footer login
tk.Label(
    login_card,
    text="✦ Moodiary by DJL  •  Dilindungi Isolasi Basis Data Multi-User ✦",
    font=FONT_SMALL,
    bg=BG_CARD_YELLOW,
    fg=TEXT_MUTED
).pack(pady=(0, 16))


# ==============================================================================
# 2. MAIN DESKTOP DASHBOARD (MAIN FRAME)
# ==============================================================================
# Sidebar Kiri (260px)
sidebar = tk.Frame(
    main_frame,
    bg=BG_CARD_YELLOW,
    width=270,
    bd=1,
    relief="solid"
)
sidebar.pack(side="left", fill="y", padx=(16, 10), pady=16)
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="🌸 MOODIARY",
    font=("Segoe UI", 18, "bold"),
    bg=BG_CARD_YELLOW,
    fg=ACCENT_PINK
).pack(pady=(22, 4), padx=16)

lbl_clock = tk.Label(
    sidebar,
    text="00:00:00",
    font=("Segoe UI", 11, "bold"),
    bg=BG_CARD_YELLOW,
    fg=TEXT_MUTED
)
lbl_clock.pack(pady=(0, 14))

profil_box = tk.Frame(sidebar, bg=BG_WHITE, bd=1, relief="solid")
profil_box.pack(fill="x", padx=16, pady=8)

lbl_profile_title = tk.Label(profil_box, text=get_text("active_profile"), font=FONT_SMALL, bg=BG_WHITE, fg=TEXT_MUTED)
lbl_profile_title.pack(anchor="w", padx=12, pady=(10, 2))
lbl_greeting = tk.Label(profil_box, text="Halo, Pengguna!", font=FONT_CARD_TITLE, bg=BG_WHITE, fg=TEXT_DARK)
lbl_greeting.pack(anchor="w", padx=12, pady=(0, 10))

# Daily Quote Card di Sidebar
quote_card = tk.Frame(sidebar, bg=BG_WHITE, bd=1, relief="solid")
quote_card.pack(fill="x", padx=16, pady=12)

lbl_insp_title = tk.Label(quote_card, text=get_text("daily_inspiration"), font=FONT_SMALL, bg=BG_WHITE, fg=ACCENT_PINK)
lbl_insp_title.pack(anchor="w", padx=12, pady=(10, 4))
quote_box = tk.Label(
    quote_card,
    text='"Percayalah pada dirimu sendiri."',
    font=FONT_ITALIC,
    bg=BG_WHITE,
    fg=TEXT_DARK,
    wraplength=210,
    justify="left"
)
quote_box.pack(anchor="w", padx=12, pady=(0, 12))

# Tombol Pengaturan & Keluar di bawah Sidebar
sidebar_bottom = tk.Frame(sidebar, bg=BG_CARD_YELLOW)
sidebar_bottom.pack(side="bottom", fill="x", padx=16, pady=20)

btn_settings = tk.Button(
    sidebar_bottom,
    text=get_text("settings"),
    command=lambda: tampilkan_fitur(
        render_settings,
        current_username=current_user,
        callback_refresh_lang=refresh_semua_teks,
        callback_refresh_user=update_active_username
    ),
    bg=PRIMARY_YELLOW,
    activebackground=PRIMARY_YELLOW_HOVER,
    font=("Segoe UI", 10, "bold"),
    fg=TEXT_DARK,
    bd=0,
    cursor="hand2",
    pady=8
)
btn_settings.pack(fill="x", pady=(0, 8))


def logout():
    global current_user
    if messagebox.askyesno("Keluar", "Apakah Anda yakin ingin keluar dari akun ini?"):
        current_user = ""
        database.set_active_user(None)
        tampilkan_login()


btn_logout = tk.Button(
    sidebar_bottom,
    text=get_text("logout"),
    command=logout,
    bg=SECONDARY_PINK,
    activebackground="#F48FB1",
    font=("Segoe UI", 10, "bold"),
    fg=ACCENT_DARK,
    bd=0,
    cursor="hand2",
    pady=8
)
btn_logout.pack(fill="x")

tk.Label(
    sidebar_bottom,
    text="✦ by DJL ✦",
    font=FONT_ITALIC,
    bg=BG_CARD_YELLOW,
    fg=ACCENT_PINK
).pack(pady=(12, 0))


# Content Panel Kanan (Grid Feature Cards 2x3)
content_frame = tk.Frame(main_frame, bg=BG_PINK)
content_frame.pack(side="left", fill="both", expand=True, padx=(8, 16), pady=16)

banner_frame = tk.Frame(content_frame, bg=BG_PINK)
banner_frame.pack(fill="x", pady=(8, 14))

banner_title_lbl = tk.Label(
    banner_frame,
    text=get_text("banner_title"),
    font=("Segoe UI", 18, "bold"),
    bg=BG_PINK,
    fg=ACCENT_PINK
)
banner_title_lbl.pack(anchor="w")

banner_sub_lbl = tk.Label(
    banner_frame,
    text=get_text("banner_subtitle"),
    font=FONT_BODY,
    bg=BG_PINK,
    fg=TEXT_DARK
)
banner_sub_lbl.pack(anchor="w", pady=(2, 0))

# 2x3 Feature Grid
grid_container = tk.Frame(content_frame, bg=BG_PINK)
grid_container.pack(fill="both", expand=True)

for i in range(2):
    grid_container.rowconfigure(i, weight=1, minsize=140)
for j in range(3):
    grid_container.columnconfigure(j, weight=1, minsize=200)


def buat_feature_card(parent, row, col, icon_teks, judul, deskripsi, command_func, card_bg=BG_CARD_YELLOW):
    card = tk.Frame(
        parent,
        bg=card_bg,
        bd=1,
        relief="solid",
        cursor="hand2"
    )
    card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    content = tk.Frame(card, bg=card_bg)
    content.pack(fill="both", expand=True, padx=16, pady=16)

    icon_lbl = tk.Label(
        content,
        text=icon_teks,
        font=("Segoe UI", 28),
        bg=card_bg
    )
    icon_lbl.pack(anchor="w", pady=(0, 8))

    title_lbl = tk.Label(
        content,
        text=judul,
        font=FONT_CARD_TITLE,
        bg=card_bg,
        fg=ACCENT_PINK
    )
    title_lbl.pack(anchor="w", pady=(0, 4))

    desc_lbl = tk.Label(
        content,
        text=deskripsi,
        font=FONT_SMALL,
        bg=card_bg,
        fg=TEXT_DARK,
        wraplength=190,
        justify="left"
    )
    desc_lbl.pack(anchor="w")

    def on_click(e=None):
        command_func()

    card.bind("<Button-1>", on_click)
    content.bind("<Button-1>", on_click)
    icon_lbl.bind("<Button-1>", on_click)
    title_lbl.bind("<Button-1>", on_click)
    desc_lbl.bind("<Button-1>", on_click)

    return title_lbl, desc_lbl


card_journal = buat_feature_card(
    grid_container, 0, 0, "📖", get_text("menu_journal_title"),
    get_text("menu_journal_desc"),
    lambda: tampilkan_fitur(render_daily_journal)
)

card_mood = buat_feature_card(
    grid_container, 0, 1, "😊", get_text("menu_mood_title"),
    get_text("menu_mood_desc"),
    lambda: tampilkan_fitur(render_mood_tracker)
)

card_todo = buat_feature_card(
    grid_container, 0, 2, "📝", get_text("menu_todo_title"),
    get_text("menu_todo_desc"),
    lambda: tampilkan_fitur(render_todo_list)
)

card_wish = buat_feature_card(
    grid_container, 1, 0, "🌟", get_text("menu_wish_title"),
    get_text("menu_wish_desc"),
    lambda: tampilkan_fitur(render_wish_list)
)

card_quote = buat_feature_card(
    grid_container, 1, 1, "💬", get_text("menu_quote_title"),
    get_text("menu_quote_desc"),
    lambda: tampilkan_fitur(render_quote)
)

card_statistik = buat_feature_card(
    grid_container, 1, 2, "📊", get_text("menu_stat_title"),
    get_text("menu_stat_desc"),
    lambda: tampilkan_fitur(render_statistik)
)


def update_waktu():
    now = datetime.now().strftime("%H:%M:%S  |  %d-%m-%Y")
    lbl_clock.config(text=now)
    app.after(1000, update_waktu)


def update_active_username(name):
    global current_user
    current_user = name
    refresh_semua_teks()


def refresh_semua_teks():
    current_lang = language.LANG

    lbl_greeting.config(text=current_user)

    quote_baru = random.choice(QUOTES[current_lang])
    quote_box.config(text=f'"{quote_baru}"')

    lbl_profile_title.config(text=get_text("active_profile"))
    lbl_insp_title.config(text=get_text("daily_inspiration"))
    btn_settings.config(text=get_text("settings"))
    btn_logout.config(text=get_text("logout"))

    banner_title_lbl.config(text=get_text("banner_title"))
    banner_sub_lbl.config(text=get_text("banner_subtitle"))

    card_journal[0].config(text=get_text("menu_journal_title"))
    card_journal[1].config(text=get_text("menu_journal_desc"))

    card_mood[0].config(text=get_text("menu_mood_title"))
    card_mood[1].config(text=get_text("menu_mood_desc"))

    card_todo[0].config(text=get_text("menu_todo_title"))
    card_todo[1].config(text=get_text("menu_todo_desc"))

    card_wish[0].config(text=get_text("menu_wish_title"))
    card_wish[1].config(text=get_text("menu_wish_desc"))

    card_quote[0].config(text=get_text("menu_quote_title"))
    card_quote[1].config(text=get_text("menu_quote_desc"))

    card_statistik[0].config(text=get_text("menu_stat_title"))
    card_statistik[1].config(text=get_text("menu_stat_desc"))



if __name__ == "__main__":
    update_waktu()
    tampilkan_login()
    app.mainloop()
