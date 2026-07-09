# manager/daily_journal.py
# ==============================================================================
# MOODIARY - DAILY JOURNAL (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import core.database as database
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

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


def render_daily_journal(parent_container, on_back_callback=None):
    """
    Merender antarmuka Daily Journal di dalam parent_container (Single-Window).
    """
    configure_ttk_styles()

    selected_id = None

    # =====================================
    # HEADER DENGAN TOMBOL KEMBALI
    # =====================================
    create_back_header(
        parent_container,
        "📖 Daily Journal",
        "Tulis refleksi, cerita, perasaan, dan kenangan berharga hari ini ✨",
        on_back_callback
    )

    # =====================================
    # MASTER-DETAIL SPLIT CONTAINER
    # =====================================
    split_container = tk.Frame(parent_container, bg=BG_PINK)
    split_container.pack(fill="both", expand=True, padx=20, pady=(4, 15))

    # ---- LEFT PANEL (MASTER LISTVIEW: SEARCH + TREEVIEW) ----
    left_panel = tk.Frame(
        split_container,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        width=430
    )
    left_panel.pack(side="left", fill="both", padx=(0, 12))
    left_panel.pack_propagate(False)

    search_frame = tk.Frame(left_panel, bg=BG_CARD_YELLOW)
    search_frame.pack(fill="x", padx=14, pady=(14, 8))

    tk.Label(
        search_frame,
        text="🔍 Cari Catatan Jurnal",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_DARK
    ).pack(anchor="w", pady=(0, 4))

    search_entry = tk.Entry(
        search_frame,
        font=("Segoe UI", 10),
        bg=BG_WHITE,
        relief="solid",
        bd=1
    )
    search_entry.pack(fill="x", ipady=3)

    tree_frame = tk.Frame(left_panel, bg=BG_CARD_YELLOW)
    tree_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    columns = ("id", "tanggal", "judul", "mood")
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    tree.heading("id", text="ID")
    tree.heading("tanggal", text="📅 Tanggal")
    tree.heading("judul", text="📝 Judul")
    tree.heading("mood", text="😊 Mood")

    tree.column("id", width=35, anchor="center")
    tree.column("tanggal", width=95, anchor="center")
    tree.column("judul", width=180)
    tree.column("mood", width=85, anchor="center")

    scrollbar = ttk.Scrollbar(
        tree_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---- RIGHT PANEL (DETAIL EDITOR CARD) ----
    right_panel = tk.Frame(
        split_container,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid"
    )
    right_panel.pack(side="right", fill="both", expand=True)

    editor_header = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    editor_header.pack(fill="x", padx=20, pady=(14, 6))

    lbl_editor_title = tk.Label(
        editor_header,
        text="✍️ Editor Catatan Jurnal",
        font=("Segoe UI", 14, "bold"),
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    )
    lbl_editor_title.pack(anchor="w")

    # Baris 1: Tanggal & Judul
    form_grid = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    form_grid.pack(fill="x", padx=20, pady=4)

    col1 = tk.Frame(form_grid, bg=BG_CARD_YELLOW, width=150)
    col1.pack(side="left", fill="x", padx=(0, 12))

    tk.Label(col1, text="📅 Tanggal", font=FONT_CARD_TITLE, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w", pady=(0, 4))
    entry_tanggal = tk.Entry(col1, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_tanggal.pack(fill="x", ipady=3)
    entry_tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))

    col2 = tk.Frame(form_grid, bg=BG_CARD_YELLOW)
    col2.pack(side="left", fill="x", expand=True)

    tk.Label(col2, text="📝 Judul Jurnal", font=FONT_CARD_TITLE, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w", pady=(0, 4))
    entry_judul = tk.Entry(col2, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_judul.pack(fill="x", ipady=3)

    # Baris 2: Mood & Kategori
    form_grid2 = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    form_grid2.pack(fill="x", padx=20, pady=8)

    col3 = tk.Frame(form_grid2, bg=BG_CARD_YELLOW)
    col3.pack(side="left", fill="x", expand=True, padx=(0, 12))

    tk.Label(col3, text="😊 Suasana Hati (Mood)", font=FONT_CARD_TITLE, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w", pady=(0, 4))
    mood_var = tk.StringVar()
    mood_combo = ttk.Combobox(
        col3,
        textvariable=mood_var,
        state="readonly",
        font=("Segoe UI", 10)
    )
    mood_combo["values"] = (
        "😍 Very Happy",
        "😊 Happy",
        "😐 Neutral",
        "😔 Sad",
        "😭 Very Sad",
        "😡 Angry",
        "😴 Tired",
        "🤩 Excited",
        "🥰 Loved"
    )
    mood_combo.pack(fill="x")
    mood_combo.current(1)

    col4 = tk.Frame(form_grid2, bg=BG_CARD_YELLOW)
    col4.pack(side="left", fill="x", expand=True)

    tk.Label(col4, text="🏷️ Kategori Catatan", font=FONT_CARD_TITLE, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w", pady=(0, 4))
    kategori_var = tk.StringVar()
    kategori_combo = ttk.Combobox(
        col4,
        textvariable=kategori_var,
        state="readonly",
        font=("Segoe UI", 10)
    )
    kategori_combo["values"] = (
        "Personal",
        "College",
        "Work",
        "Goals",
        "Memories",
        "Gratitude"
    )
    kategori_combo.pack(fill="x")
    kategori_combo.current(0)

    # Action Buttons Bar (Ditempatkan dengan side='bottom' agar SELALU TERLIHAT di bawah)
    btn_bar = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    btn_bar.pack(side="bottom", fill="x", padx=20, pady=(10, 16))

    btn_style = {
        "font": ("Segoe UI", 10, "bold"),
        "bd": 0,
        "cursor": "hand2",
        "pady": 8
    }

    tk.Button(
        btn_bar,
        text="💾 Simpan Baru",
        command=lambda: tambah(),
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        fg=TEXT_DARK,
        width=14,
        **btn_style
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        btn_bar,
        text="✏️ Update",
        command=lambda: update(),
        bg=BTN_UPDATE,
        activebackground="#81D4FA",
        fg=TEXT_DARK,
        width=12,
        **btn_style
    ).pack(side="left", padx=8)

    tk.Button(
        btn_bar,
        text="🗑️ Hapus",
        command=lambda: hapus(),
        bg=BTN_DELETE,
        activebackground="#EF9A9A",
        fg=TEXT_DARK,
        width=11,
        **btn_style
    ).pack(side="left", padx=8)

    tk.Button(
        btn_bar,
        text="🔄 Clear Form",
        command=lambda: clear_form(),
        bg=BTN_CLEAR,
        activebackground="#CE93D8",
        fg=TEXT_DARK,
        width=12,
        **btn_style
    ).pack(side="left", padx=8)

    # Isi Catatan Jurnal (Dipack setelah tombol bawah agar mengambil sisa ruang di tengah)
    body_frame = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    body_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(2, 8))

    tk.Label(
        body_frame,
        text="📖 Isi Cerita & Refleksimu",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", pady=(0, 4))

    txt_journal = tk.Text(
        body_frame,
        font=("Segoe UI", 10),
        bg=BG_WHITE,
        relief="solid",
        bd=1,
        wrap="word",
        padx=12,
        pady=12
    )
    txt_journal.pack(fill="both", expand=True)

    char_label = tk.Label(
        body_frame,
        text="0 karakter",
        bg=BG_CARD_YELLOW,
        fg=TEXT_MUTED,
        font=FONT_SMALL
    )
    char_label.pack(anchor="e", pady=(4, 0))

    def update_counter(event=None):
        jumlah = len(txt_journal.get("1.0", tk.END).strip())
        char_label.config(text=f"{jumlah} karakter")

    txt_journal.bind("<KeyRelease>", update_counter)

    # =====================================
    # TAMPILKAN DATA PADA TREEVIEW
    # =====================================
    def tampilkan_data(keyword=""):
        for item in tree.get_children():
            tree.delete(item)

        conn = database.get_db_connection()
        cursor = conn.cursor()

        if keyword:
            cursor.execute("""
            SELECT id, tanggal, judul, mood
            FROM journal
            WHERE judul LIKE ? OR isi LIKE ? OR kategori LIKE ?
            ORDER BY id DESC
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        else:
            cursor.execute("""
            SELECT id, tanggal, judul, mood
            FROM journal
            ORDER BY id DESC
            """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

    def on_search(event=None):
        tampilkan_data(search_entry.get().strip())

    search_entry.bind("<KeyRelease>", on_search)

    def pilih_data(event):
        nonlocal selected_id
        pilihan = tree.selection()
        if not pilihan:
            return

        item_id = tree.item(pilihan[0], "values")[0]
        selected_id = int(item_id)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM journal WHERE id=?", (selected_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return

        lbl_editor_title.config(text=f"✍️ Editor Jurnal (ID: #{selected_id})")

        entry_tanggal.delete(0, tk.END)
        entry_tanggal.insert(0, row[1])

        entry_judul.delete(0, tk.END)
        entry_judul.insert(0, row[2])

        txt_journal.delete("1.0", tk.END)
        txt_journal.insert(tk.END, row[3])

        mood_combo.set(row[4])
        kategori_combo.set(row[5])

        update_counter()

    tree.bind("<<TreeviewSelect>>", pilih_data)

    def tambah():
        tanggal = entry_tanggal.get().strip()
        judul = entry_judul.get().strip()
        isi = txt_journal.get("1.0", tk.END).strip()
        mood = mood_var.get()
        kategori = kategori_var.get()

        if judul == "" or isi == "":
            messagebox.showwarning("Warning", "Harap isi judul dan isi catatan jurnal.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO journal (tanggal, judul, isi, mood, kategori)
        VALUES (?, ?, ?, ?, ?)
        """, (tanggal, judul, isi, mood, kategori))
        conn.commit()
        conn.close()

        clear_form()
        tampilkan_data()
        messagebox.showinfo("Success", "🎉 Catatan jurnal berhasil disimpan!")

    def update():
        if selected_id is None:
            messagebox.showwarning("Warning", "Pilih catatan jurnal dari daftar di kiri terlebih dahulu.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE journal
        SET tanggal=?, judul=?, isi=?, mood=?, kategori=?
        WHERE id=?
        """, (
            entry_tanggal.get().strip(),
            entry_judul.get().strip(),
            txt_journal.get("1.0", tk.END).strip(),
            mood_var.get(),
            kategori_var.get(),
            selected_id
        ))
        conn.commit()
        conn.close()

        tampilkan_data()
        messagebox.showinfo("Success", "Catatan jurnal berhasil diperbarui.")

    def hapus():
        if selected_id is None:
            messagebox.showwarning("Warning", "Pilih catatan jurnal yang ingin dihapus.")
            return

        if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus catatan ini?"):
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM journal WHERE id=?", (selected_id,))
        conn.commit()
        conn.close()

        clear_form()
        tampilkan_data()

    def clear_form():
        nonlocal selected_id
        selected_id = None
        lbl_editor_title.config(text="✍️ Editor Catatan Jurnal")
        entry_judul.delete(0, tk.END)
        txt_journal.delete("1.0", tk.END)
        mood_combo.current(1)
        kategori_combo.current(0)
        update_counter()

    tampilkan_data()


def klik_daily_journal(parent_container=None, on_back_callback=None):
    if parent_container:
        render_daily_journal(parent_container, on_back_callback)
    else:
        win = tk.Toplevel()
        win.title("📖 Daily Journal - Catatan Harian Moodiary")
        win.configure(bg=BG_PINK)
        center_window(win, 1080, 740)
        render_daily_journal(win, None)
