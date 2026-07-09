# manager/todolist.py
# ==============================================================================
# MOODIARY - TO-DO LIST (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import core.database as database
import tkinter as tk
from tkinter import ttk, messagebox
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


def render_todo_list(parent_container, on_back_callback=None):
    """
    Merender antarmuka To-Do List di dalam parent_container (Single-Window).
    """
    configure_ttk_styles()

    selected_id = None

    # ==================================
    # HEADER DENGAN TOMBOL KEMBALI
    # ==================================
    create_back_header(
        parent_container,
        "📝 Professional Task & To-Do List",
        "Kelola prioritas tugas harian, batas waktu (deadline), dan status penyelesaianmu ✨",
        on_back_callback
    )

    # ==================================
    # REMINDER ALERT BANNER
    # ==================================
    alert_banner = tk.Frame(parent_container, bg="#FFF3E0", bd=1, relief="solid")
    alert_banner.pack(fill="x", padx=20, pady=(0, 10))

    lbl_alert_text = tk.Label(
        alert_banner,
        text="⏳ Memeriksa tenggat waktu tugas aktif...",
        font=("Segoe UI", 9, "bold"),
        bg="#FFF3E0",
        fg="#E65100",
        pady=8,
        padx=12
    )
    lbl_alert_text.pack(anchor="w")

    def periksa_deadline():
        conn = database.get_db_connection()
        cursor = conn.cursor()
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        SELECT COUNT(*) FROM todo
        WHERE selesai=0 AND deadline <= ? AND deadline != ''
        """, (today_str,))
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            lbl_alert_text.config(
                text=f"🚨 PERHATIAN: Terdapat {count} tugas aktif yang jatuh tempo hari ini atau telah melewati batas waktu (Deadline)!"
            )
            alert_banner.config(bg="#FFEBEE")
            lbl_alert_text.config(bg="#FFEBEE", fg="#C62828")
        else:
            lbl_alert_text.config(
                text="✅ Seluruh tugas aktif dalam jadwal terkendali dengan baik."
            )
            alert_banner.config(bg="#E8F5E9")
            lbl_alert_text.config(bg="#E8F5E9", fg="#2E7D32")

    # ==================================
    # KARTU FORM INPUT TUGAS
    # ==================================
    form_card = tk.Frame(parent_container, bg=BG_CARD_YELLOW, bd=1, relief="solid")
    form_card.pack(fill="x", padx=20, pady=4)

    lbl_form_title = tk.Label(
        form_card,
        text="➕ Tambah / Perbarui Tugas",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    )
    lbl_form_title.pack(anchor="w", padx=16, pady=(12, 8))

    grid_frame = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    grid_frame.pack(fill="x", padx=16, pady=(0, 12))

    col1 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW)
    col1.pack(side="left", fill="x", expand=True, padx=(0, 12))

    tk.Label(col1, text="📌 Nama Tugas", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    entry_tugas = tk.Entry(col1, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_tugas.pack(fill="x", pady=(2, 0), ipady=4)

    col2 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW, width=150)
    col2.pack(side="left", fill="x", padx=(0, 12))

    tk.Label(col2, text="📅 Deadline (YYYY-MM-DD)", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    entry_deadline = tk.Entry(col2, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_deadline.pack(fill="x", pady=(2, 0), ipady=4)
    entry_deadline.insert(0, datetime.now().strftime("%Y-%m-%d"))

    col3 = tk.Frame(grid_frame, bg=BG_CARD_YELLOW, width=150)
    col3.pack(side="left", fill="x")

    tk.Label(col3, text="🔥 Prioritas", font=FONT_SMALL, bg=BG_CARD_YELLOW, fg=TEXT_DARK).pack(anchor="w")
    prioritas_var = tk.StringVar()
    combo_prio = ttk.Combobox(
        col3,
        textvariable=prioritas_var,
        values=("🔴 High Priority", "🟡 Medium Priority", "🟢 Low Priority"),
        state="readonly",
        font=("Segoe UI", 10)
    )
    combo_prio.pack(fill="x", pady=(2, 0))
    combo_prio.current(1)

    # AKSI TOMBOL FORM
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
        text="💾 Simpan Tugas",
        command=lambda: simpan_tugas(),
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        fg=TEXT_DARK,
        width=14,
        **btn_style
    ).pack(side="left", padx=(0, 6))

    tk.Button(
        btn_bar,
        text="✏️ Update Tugas",
        command=lambda: update_tugas(),
        bg=BTN_UPDATE,
        activebackground="#81D4FA",
        fg=TEXT_DARK,
        width=14,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🗑️ Hapus Tugas",
        command=lambda: hapus_tugas(),
        bg=BTN_DELETE,
        activebackground="#EF9A9A",
        fg=TEXT_DARK,
        width=13,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="✅ Tandai Selesai / Belum",
        command=lambda: toggle_selesai(),
        bg="#A5D6A7",
        activebackground="#81C784",
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
    # DAFTAR TUGAS DALAM TREEVIEW
    # ==================================
    list_card = tk.Frame(parent_container, bg=BG_CARD_YELLOW, bd=1, relief="solid")
    list_card.pack(fill="both", expand=True, padx=20, pady=(10, 16))

    list_header = tk.Frame(list_card, bg=BG_CARD_YELLOW)
    list_header.pack(fill="x", padx=16, pady=(12, 8))

    tk.Label(
        list_header,
        text="📋 Daftar Tugas Aktif & Selesai",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(side="left")

    cols = ("id", "tugas", "deadline", "prioritas", "selesai")
    tree_todo = ttk.Treeview(
        list_card,
        columns=cols,
        show="headings",
        selectmode="browse"
    )

    tree_todo.heading("id", text="ID")
    tree_todo.heading("tugas", text="📌 Nama Tugas")
    tree_todo.heading("deadline", text="📅 Deadline")
    tree_todo.heading("prioritas", text="🔥 Prioritas")
    tree_todo.heading("selesai", text="Status")

    tree_todo.column("id", width=35, anchor="center")
    tree_todo.column("tugas", width=360)
    tree_todo.column("deadline", width=110, anchor="center")
    tree_todo.column("prioritas", width=140, anchor="center")
    tree_todo.column("selesai", width=120, anchor="center")

    scroll_y = ttk.Scrollbar(list_card, orient="vertical", command=tree_todo.yview)
    tree_todo.configure(yscrollcommand=scroll_y.set)

    tree_todo.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 14))
    scroll_y.pack(side="right", fill="y", padx=(0, 16), pady=(0, 14))

    def load_data():
        for item in tree_todo.get_children():
            tree_todo.delete(item)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, tugas, deadline, prioritas, selesai
        FROM todo
        ORDER BY selesai ASC, deadline ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            status_txt = "✅ SELESAI" if r[4] else "⏳ Belum"
            tree_todo.insert("", tk.END, values=(r[0], r[1], r[2] or "-", r[3] or "🟡 Medium Priority", status_txt))

        periksa_deadline()

    def pilih_item(event):
        nonlocal selected_id
        selected = tree_todo.selection()
        if not selected:
            return

        vals = tree_todo.item(selected[0], "values")
        selected_id = int(vals[0])
        lbl_form_title.config(text=f"✏️ Perbarui Tugas (ID: #{selected_id})")

        entry_tugas.delete(0, tk.END)
        entry_tugas.insert(0, vals[1])

        entry_deadline.delete(0, tk.END)
        entry_deadline.insert(0, vals[2] if vals[2] != "-" else "")

        combo_prio.set(vals[3])

    tree_todo.bind("<<TreeviewSelect>>", pilih_item)

    def simpan_tugas():
        tugas = entry_tugas.get().strip()
        deadline = entry_deadline.get().strip()
        prioritas = prioritas_var.get()

        if not tugas:
            messagebox.showwarning("Peringatan", "Nama tugas tidak boleh kosong.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO todo (tugas, deadline, prioritas, selesai)
        VALUES (?, ?, ?, 0)
        """, (tugas, deadline, prioritas))
        conn.commit()
        conn.close()

        clear_form()
        load_data()

    def update_tugas():
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin diperbarui dari daftar.")
            return

        tugas = entry_tugas.get().strip()
        deadline = entry_deadline.get().strip()
        prioritas = prioritas_var.get()

        if not tugas:
            messagebox.showwarning("Peringatan", "Nama tugas tidak boleh kosong.")
            return

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE todo
        SET tugas=?, deadline=?, prioritas=?
        WHERE id=?
        """, (tugas, deadline, prioritas, selected_id))
        conn.commit()
        conn.close()

        clear_form()
        load_data()

    def hapus_tugas():
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin dihapus dari daftar.")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus tugas ini?"):
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todo WHERE id=?", (selected_id,))
            conn.commit()
            conn.close()

            clear_form()
            load_data()

    def toggle_selesai():
        selected = tree_todo.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih tugas dari daftar untuk mengubah statusnya.")
            return

        vals = tree_todo.item(selected[0], "values")
        item_id = int(vals[0])
        status_kini = 1 if "SELESAI" in vals[4] else 0
        status_baru = 0 if status_kini == 1 else 1

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todo SET selesai=? WHERE id=?", (status_baru, item_id))
        conn.commit()
        conn.close()

        load_data()

    def clear_form():
        nonlocal selected_id
        selected_id = None
        lbl_form_title.config(text="➕ Tambah / Perbarui Tugas")
        entry_tugas.delete(0, tk.END)
        entry_deadline.delete(0, tk.END)
        entry_deadline.insert(0, datetime.now().strftime("%Y-%m-%d"))
        combo_prio.current(1)

    load_data()


def buka_todo(parent_container=None, on_back_callback=None):
    if parent_container:
        render_todo_list(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("📝 To-Do List & Task Manager - Moodiary")
        window.configure(bg=BG_PINK)
        center_window(window, 1080, 740)
        render_todo_list(window, None)
        