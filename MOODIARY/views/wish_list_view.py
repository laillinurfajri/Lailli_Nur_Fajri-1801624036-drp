# manager/wish_list.py
# ==============================================================================
# MOODIARY - WISH LIST & GOALS TRACKER (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import core.database as database
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from core.theme import (
    BG_PINK, BG_CARD_YELLOW, BG_WHITE,
    PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER,
    SECONDARY_PINK,
    ACCENT_PINK, ACCENT_DARK,
    TEXT_DARK, TEXT_MUTED,
    BORDER_YELLOW,
    BTN_SAVE, BTN_UPDATE, BTN_DELETE, BTN_CLEAR,
    FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY, FONT_SMALL,
    center_window, configure_ttk_styles, create_back_header
)


def render_wish_list(parent_container, on_back_callback=None):
    """
    Merender antarmuka Wish List di dalam parent_container (Single-Window).
    """
    configure_ttk_styles()

    selected_id = None

    # ==================================
    # HEADER DENGAN TOMBOL KEMBALI
    # ==================================
    create_back_header(
        parent_container,
        "🌟 Wish List & Future Dreams",
        "Catat impian, target masa depan, dan lacak progres pencapaianmu ✨",
        on_back_callback
    )

    # ==================================
    # PROGRESS INDICATOR BANNER
    # ==================================
    progress_card = tk.Frame(parent_container, bg=BG_CARD_YELLOW, bd=1, relief="solid")
    progress_card.pack(fill="x", padx=20, pady=(0, 10))

    lbl_stat = tk.Label(
        progress_card,
        text="📊 Statistik Impian: Memuat...",
        font=("Segoe UI", 10, "bold"),
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK,
        pady=8,
        padx=14
    )
    lbl_stat.pack(anchor="w")

    def update_stat_banner():
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), SUM(tercapai) FROM wish")
        total, tercapai = cursor.fetchone()
        conn.close()

        total = total or 0
        tercapai = tercapai or 0
        persen = int((tercapai / total) * 100) if total > 0 else 0

        lbl_stat.config(
            text=f"📊 Progres Impian Tercapai: {tercapai} dari {total} Impian ({persen}%) ✨ Terus semangat mewujudkan mimpimu!"
        )

    # ==================================
    # INPUT FORM CARD
    # ==================================
    form_card = tk.Frame(parent_container, bg=BG_CARD_YELLOW, bd=1, relief="solid")
    form_card.pack(fill="x", padx=20, pady=4)

    lbl_form_title = tk.Label(
        form_card,
        text="✨ Tambah Impian / Target Baru",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    )
    lbl_form_title.pack(anchor="w", padx=16, pady=(12, 8))

    grid_frame = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    grid_frame.pack(fill="x", padx=16, pady=(0, 12))

    col1 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW)
    col1.pack(side="left", fill="x", expand=True, padx=(0, 12))

    tk.Label(col1, text="🌟 Nama Impian / Keinginan", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    entry_wish = tk.Entry(col1, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_wish.pack(fill="x", pady=(2, 0), ipady=4)

    col2 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW, width=170)
    col2.pack(side="left", fill="x", padx=(0, 12))

    tk.Label(col2, text="🏷️ Kategori", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    kategori_var = tk.StringVar()
    combo_kat = ttk.Combobox(
        col2,
        textvariable=kategori_var,
        values=("Personal Goal", "Career & Education", "Travel & Adventure", "Self-Improvement", "Financial", "General"),
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_kat.pack(fill="x", pady=(2, 0))
    combo_kat.current(0)

    col3 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW, width=150)
    col3.pack(side="left", fill="x")

    tk.Label(col3, text="🔥 Prioritas Target", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    prioritas_var = tk.StringVar()
    combo_prio = ttk.Combobox(
        col3,
        textvariable=prioritas_var,
        values=("Tinggi (Urgent)", "Sedang (Important)", "Santai (Long-term)"),
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_prio.pack(fill="x", pady=(2, 0))
    combo_prio.current(1)

    btn_bar = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    btn_bar.pack(fill="x", padx=16, pady=(4, 14))

    btn_style = {
        "font": ("Segoe UI", 9, "bold"),
        "bd": 0,
        "cursor": "hand2",
        "pady": 7
    }

    tk.Button(
        btn_bar,
        text="💾 Simpan Impian",
        command=lambda: simpan_wish(),
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        fg=TEXT_DARK,
        width=14,
        **btn_style
    ).pack(side="left", padx=(0, 6))

    tk.Button(
        btn_bar,
        text="✏️ Update Impian",
        command=lambda: update_wish(),
        bg=BTN_UPDATE,
        activebackground="#81D4FA",
        fg=TEXT_DARK,
        width=14,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🗑️ Hapus Impian",
        command=lambda: hapus_wish(),
        bg=BTN_DELETE,
        activebackground="#EF9A9A",
        fg=TEXT_DARK,
        width=13,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🎉 Tandai Tercapai / Belum",
        command=lambda: toggle_tercapai(),
        bg="#FFE082",
        activebackground="#FFD54F",
        fg=TEXT_DARK,
        width=21,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🔄 Clear",
        command=lambda: clear_form(),
        bg=BTN_CLEAR,
        activebackground="#CE93D8",
        fg=TEXT_DARK,
        width=9,
        **btn_style
    ).pack(side="left", padx=6)

    # ==================================
    # TABEL DAFTAR WISH LIST
    # ==================================
    list_card = tk.Frame(parent_container, bg=BG_CARD_YELLOW, bd=1, relief="solid")
    list_card.pack(fill="both", expand=True, padx=20, pady=(10, 16))

    list_header = tk.Frame(list_card, bg=BG_CARD_YELLOW)
    list_header.pack(fill="x", padx=16, pady=(12, 8))

    tk.Label(
        list_header,
        text="📋 Daftar Impianmu",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(side="left")

    cols = ("id", "wish", "kategori", "prioritas", "tercapai")
    tree_wish = ttk.Treeview(
        list_card,
        columns=cols,
        show="headings",
        selectmode="browse"
    )

    tree_wish.heading("id", text="ID")
    tree_wish.heading("wish", text="🌟 Nama Impian")
    tree_wish.heading("kategori", text="🏷️ Kategori")
    tree_wish.heading("prioritas", text="🔥 Prioritas")
    tree_wish.heading("tercapai", text="Status")

    tree_wish.column("id", width=35, anchor="center")
    tree_wish.column("wish", width=360)
    tree_wish.column("kategori", width=140, anchor="center")
    tree_wish.column("prioritas", width=140, anchor="center")
    tree_wish.column("tercapai", width=120, anchor="center")

    scroll_y = ttk.Scrollbar(list_card, orient="vertical", command=tree_wish.yview)
    tree_wish.configure(yscrollcommand=scroll_y.set)
   
    tree_wish.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 14))
    scroll_y.pack(side="right", fill="y", padx=(0, 16), pady=(0, 14))

    def load_data():
        for item in tree_wish.get_children():
            tree_wish.delete(item)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, isi, kategori, prioritas, tercapai
        FROM wish
        ORDER BY tercapai ASC, id DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            status_txt = "🎉 TERCAPAI" if r[4] else "⏳ Belum"
            tree_wish.insert("", tk.END, values=(r[0], r[1], r[2] or "General", r[3] or "Sedang", status_txt))

        update_stat_banner()

    def pilih_item(event):
        nonlocal selected_id
        selected = tree_wish.selection()
        if not selected:
            return

        vals = tree_wish.item(selected[0], "values")
        selected_id = int(vals[0])
        lbl_form_title.config(text=f"✏️ Perbarui Impian (ID: #{selected_id})")

        entry_wish.delete(0, tk.END)
        entry_wish.insert(0, vals[1])
        combo_kat.set(vals[2])
        combo_prio.set(vals[3])

    tree_wish.bind("<<TreeviewSelect>>", pilih_item)

    def simpan_wish():
        wish = entry_wish.get().strip()
        kategori = kategori_var.get()
        prioritas = prioritas_var.get()

        if not wish:
            messagebox.showwarning("Peringatan", "Nama impian tidak boleh kosong.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO wish (isi, kategori, prioritas, tercapai)
        VALUES (?, ?, ?, 0)
        """, (wish, kategori, prioritas))
        conn.commit()
        conn.close()

        clear_form()
        load_data()

    def update_wish():
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih impian yang ingin diperbarui dari daftar.")
            return

        wish = entry_wish.get().strip()
        kategori = kategori_var.get()
        prioritas = prioritas_var.get()

        if not wish:
            messagebox.showwarning("Peringatan", "Nama impian tidak boleh kosong.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE wish
        SET isi=?, kategori=?, prioritas=?
        WHERE id=?
        """, (wish, kategori, prioritas, selected_id))
        conn.commit()
        conn.close()

        clear_form()
        load_data()

    def hapus_wish():
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih impian yang ingin dihapus dari daftar.")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus impian ini?"):
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM wish WHERE id=?", (selected_id,))
            conn.commit()
            conn.close()

            clear_form()
            load_data()

    def toggle_tercapai():
        selected = tree_wish.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih impian dari daftar untuk mengubah status pencapaiannya.")
            return

        vals = tree_wish.item(selected[0], "values")
        item_id = int(vals[0])
        status_kini = 1 if "TERCAPAI" in vals[4] else 0
        status_baru = 0 if status_kini == 1 else 1

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE wish SET tercapai=? WHERE id=?", (status_baru, item_id))
        conn.commit()
        conn.close()

        if status_baru == 1:
            messagebox.showinfo("🎉 Selamat!", "Luar biasa! Satu lagi impian berhargamu telah berhasil dicapai!")

        load_data()

    def clear_form():
        nonlocal selected_id
        selected_id = None
        lbl_form_title.config(text="✨ Tambah Impian / Target Baru")
        entry_wish.delete(0, tk.END)
        combo_kat.current(0)
        combo_prio.current(1)

    load_data()


def klik_wish_list(parent_container=None, on_back_callback=None):
    if parent_container:
        render_wish_list(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("🌟 Wish List & Goals Tracker - Moodiary")
        window.configure(bg=BG_PINK)
        center_window(window, 1080, 740)
        render_wish_list(window, None)


klik_wish_journal = klik_wish_list
