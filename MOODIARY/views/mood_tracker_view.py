# manager/mood_tracker.py
# ==============================================================================
# MOODIARY - MOOD TRACKER & CALENDAR (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import core.database as database
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import calendar
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


def render_mood_tracker(parent_container, on_back_callback=None):
    """
    Merender antarmuka Mood Tracker di dalam parent_container (Single-Window).
    """
    configure_ttk_styles()

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    selected_date_str = now.strftime("%Y-%m-%d")
    selected_id = None

    # ==================================
    # HEADER DENGAN TOMBOL KEMBALI
    # ==================================
    create_back_header(
        parent_container,
        "😊 Mood Tracker & Visual Calendar",
        "Lacak dan pantau tren emosimu setiap hari melalui kalender interaktif ✨",
        on_back_callback
    )

    # ==================================
    # MAIN SPLIT CONTAINER
    # ==================================
    main_split = tk.Frame(parent_container, bg=BG_PINK)
    main_split.pack(fill="both", expand=True, padx=20, pady=(0, 14))

    # --- LEFT PANEL: KALENDER INTERAKTIF ---
    left_panel = tk.Frame(
        main_split,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid",
        width=480
    )
    left_panel.pack(side="left", fill="both", padx=(0, 12))
    left_panel.pack_propagate(False)

    cal_header = tk.Frame(left_panel, bg=BG_CARD_YELLOW)
    cal_header.pack(fill="x", padx=16, pady=(16, 10))

    lbl_month_year = tk.Label(
        cal_header,
        text="",
        font=("Segoe UI", 13, "bold"),
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    )
    lbl_month_year.pack(side="left")

    btn_cal_nav = tk.Frame(cal_header, bg=BG_CARD_YELLOW)
    btn_cal_nav.pack(side="right")

    tk.Button(
        btn_cal_nav,
        text="◀",
        font=("Segoe UI", 9, "bold"),
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        bd=0,
        cursor="hand2",
        width=3,
        command=lambda: change_month(-1)
    ).pack(side="left", padx=2)

    tk.Button(
        btn_cal_nav,
        text="▶",
        font=("Segoe UI", 9, "bold"),
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        bd=0,
        cursor="hand2",
        width=3,
        command=lambda: change_month(1)
    ).pack(side="left", padx=2)

    # Hari dalam seminggu
    days_header_frame = tk.Frame(left_panel, bg=BG_CARD_YELLOW)
    days_header_frame.pack(fill="x", padx=14)
    hari_indo = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    for i, h in enumerate(hari_indo):
        tk.Label(
            days_header_frame,
            text=h,
            font=("Segoe UI", 9, "bold"),
            bg=BG_CARD_YELLOW,
            fg=ACCENT_DARK,
            width=6
        ).grid(row=0, column=i, pady=4)

    cal_grid_frame = tk.Frame(left_panel, bg=BG_CARD_YELLOW)
    cal_grid_frame.pack(fill="both", expand=True, padx=14, pady=(2, 14))

    # --- RIGHT PANEL: FORM DAN RIWAYAT ---
    right_panel = tk.Frame(
        main_split,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid"
    )
    right_panel.pack(side="right", fill="both", expand=True)

    form_card = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    form_card.pack(fill="x", padx=20, pady=(16, 10))

    lbl_selected_date = tk.Label(
        form_card,
        text=f"📅 Tanggal Terpilih: {selected_date_str}",
        font=("Segoe UI", 12, "bold"),
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    )
    lbl_selected_date.pack(anchor="w", pady=(0, 10))

    mood_options = [
        ("😍 Sangat Bahagia", "😍 Very Happy", "#F8BBD0"),
        ("😊 Bahagia", "😊 Happy", "#FFF59D"),
        ("😐 Biasa Saja", "😐 Neutral", "#E0E0E0"),
        ("😔 Sedih", "😔 Sad", "#90CAF9"),
        ("😭 Sangat Sedih", "😭 Very Sad", "#64B5F6"),
        ("😡 Marah", "😡 Angry", "#EF9A9A"),
        ("😴 Lelah", "😴 Tired", "#BCAAA4"),
        ("🤩 Bersemangat", "🤩 Excited", "#FFF176"),
        ("🥰 Penuh Cinta", "🥰 Loved", "#F48FB1"),
        ("🧘 Tenang", "🧘 Calm", "#A5D6A7")
    ]

    selected_mood_val = tk.StringVar(value="😊 Happy")

    mood_grid = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    mood_grid.pack(fill="x", pady=4)

    for idx, (label_id, val_en, col_hex) in enumerate(mood_options):
        r = idx // 2
        c = idx % 2
        rb = tk.Radiobutton(
            mood_grid,
            text=label_id,
            variable=selected_mood_val,
            value=val_en,
            font=FONT_BODY,
            bg=BG_CARD_YELLOW,
            activebackground=BG_CARD_YELLOW,
            cursor="hand2",
            selectcolor=BG_WHITE
        )
        rb.grid(row=r, column=c, sticky="w", padx=10, pady=2)

    catatan_frame = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    catatan_frame.pack(fill="x", pady=(10, 4))

    tk.Label(
        catatan_frame,
        text="📝 Catatan Tambahan (Opsional):",
        font=FONT_SMALL,
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w")

    entry_catatan = tk.Entry(
        catatan_frame,
        font=("Segoe UI", 10),
        bg=BG_WHITE,
        relief="solid",
        bd=1
    )
    entry_catatan.pack(fill="x", pady=(2, 8), ipady=4)

    def simpan_mood():
        catatan = entry_catatan.get().strip()
        mood_val = selected_mood_val.get()

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO mood (tanggal, mood, catatan)
        VALUES (?, ?, ?)
        """, (selected_date_str, mood_val, catatan))
        conn.commit()
        conn.close()

        clear_form()
        render_cal_grid()
        refresh_history()
        messagebox.showinfo("Tersimpan", f"🌸 Mood untuk tanggal {selected_date_str} berhasil dicatat!")

    def update_mood():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data mood dari riwayat di bawah terlebih dahulu untuk diupdate.")
            return

        catatan = entry_catatan.get().strip()
        mood_val = selected_mood_val.get()

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE mood
        SET tanggal=?, mood=?, catatan=?
        WHERE id=?
        """, (selected_date_str, mood_val, catatan, selected_id))
        conn.commit()
        conn.close()

        clear_form()
        render_cal_grid()
        refresh_history()
        messagebox.showinfo("Diperbarui", "🎉 Catatan mood berhasil diperbarui!")

    def hapus_mood():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data mood dari riwayat di bawah yang ingin dihapus.")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus catatan mood ini?"):
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mood WHERE id=?", (selected_id,))
            conn.commit()
            conn.close()

            clear_form()
            render_cal_grid()
            refresh_history()

    def clear_form():
        nonlocal selected_id
        selected_id = None
        lbl_selected_date.config(text=f"📅 Tanggal Terpilih: {selected_date_str}")
        entry_catatan.delete(0, tk.END)
        selected_mood_val.set("😊 Happy")

    btn_bar = tk.Frame(form_card, bg=BG_CARD_YELLOW)
    btn_bar.pack(fill="x", pady=(2, 8))

    btn_style = {
        "font": ("Segoe UI", 9, "bold"),
        "bd": 0,
        "cursor": "hand2",
        "pady": 7
    }

    tk.Button(
        btn_bar,
        text="💾 Simpan Baru",
        command=simpan_mood,
        bg=BTN_SAVE,
        activebackground=PRIMARY_YELLOW_HOVER,
        fg=TEXT_DARK,
        width=15,
        **btn_style
    ).pack(side="left", padx=(0, 6))

    tk.Button(
        btn_bar,
        text="✏️ Update",
        command=update_mood,
        bg=BTN_UPDATE,
        activebackground="#81D4FA",
        fg=TEXT_DARK,
        width=12,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🗑️ Hapus",
        command=hapus_mood,
        bg=BTN_DELETE,
        activebackground="#EF9A9A",
        fg=TEXT_DARK,
        width=11,
        **btn_style
    ).pack(side="left", padx=6)

    tk.Button(
        btn_bar,
        text="🔄 Clear",
        command=clear_form,
        bg=BTN_CLEAR,
        activebackground="#CE93D8",
        fg=TEXT_DARK,
        width=11,
        **btn_style
    ).pack(side="left", padx=6)

    # TABEL RIWAYAT MOOD
    history_frame = tk.Frame(right_panel, bg=BG_CARD_YELLOW)
    history_frame.pack(fill="both", expand=True, padx=20, pady=(6, 16))

    tk.Label(
        history_frame,
        text="📋 Riwayat Mood Terakhir",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(0, 6))

    cols = ("id", "tanggal", "mood", "catatan")
    tree_history = ttk.Treeview(
        history_frame,
        columns=cols,
        show="headings",
        selectmode="browse",
        height=5
    )

    tree_history.heading("id", text="ID")
    tree_history.heading("tanggal", text="📅 Tanggal")
    tree_history.heading("mood", text="😊 Mood")
    tree_history.heading("catatan", text="📝 Catatan")

    tree_history.column("id", width=35, anchor="center")
    tree_history.column("tanggal", width=95, anchor="center")
    tree_history.column("mood", width=110, anchor="center")
    tree_history.column("catatan", width=190)

    scroll_hist = ttk.Scrollbar(
        history_frame,
        orient="vertical",
        command=tree_history.yview
    )
    tree_history.configure(yscrollcommand=scroll_hist.set)

    tree_history.pack(side="left", fill="both", expand=True)
    scroll_hist.pack(side="right", fill="y")

    def refresh_history():
        for item in tree_history.get_children():
            tree_history.delete(item)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tanggal, mood, catatan FROM mood ORDER BY id DESC LIMIT 25")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            tree_history.insert("", tk.END, values=(r[0], r[1], r[2], r[3] or ""))

    def pilih_mood(event):
        nonlocal selected_id, selected_date_str
        selected = tree_history.selection()
        if not selected:
            return

        vals = tree_history.item(selected[0], "values")
        selected_id = int(vals[0])
        selected_date_str = vals[1]

        lbl_selected_date.config(text=f"✏️ Edit Mood (ID: #{selected_id}) - Tanggal: {selected_date_str}")

        mood_txt = vals[2]
        selected_mood_val.set(mood_txt)

        entry_catatan.delete(0, tk.END)
        entry_catatan.insert(0, vals[3] if len(vals) > 3 else "")

        render_cal_grid()

    tree_history.bind("<<TreeviewSelect>>", pilih_mood)

    def render_cal_grid():
        nonlocal selected_date_str

        for widget in cal_grid_frame.winfo_children():
            widget.destroy()

        nama_bulan = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        lbl_month_year.config(text=f"{nama_bulan[current_month]} {current_year}")

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tanggal, mood FROM mood WHERE tanggal LIKE ?", (f"{current_year:04d}-{current_month:02d}-%",))
        mood_data = dict(cursor.fetchall())
        conn.close()

        cal = calendar.monthcalendar(current_year, current_month)

        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day == 0:
                    continue

                date_str = f"{current_year:04d}-{current_month:02d}-{day:02d}"
                mood_day = mood_data.get(date_str, "")

                cell_bg = BG_WHITE
                fg_col = TEXT_DARK
                border_w = 1

                if mood_day:
                    cell_bg = PRIMARY_YELLOW
                if date_str == selected_date_str:
                    cell_bg = "#F8BBD0"
                    border_w = 2

                btn_day = tk.Button(
                    cal_grid_frame,
                    text=f"{day}\n{mood_day[:2] if mood_day else ''}",
                    font=("Segoe UI", 9, "bold" if date_str == selected_date_str else "normal"),
                    bg=cell_bg,
                    fg=fg_col,
                    relief="solid",
                    bd=border_w,
                    cursor="hand2",
                    command=lambda d=date_str: select_date(d)
                )
                btn_day.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

        for i in range(7):
            cal_grid_frame.columnconfigure(i, weight=1)
        for i in range(len(cal)):
            cal_grid_frame.rowconfigure(i, weight=1)

    def select_date(d_str):
        nonlocal selected_date_str
        selected_date_str = d_str
        lbl_selected_date.config(text=f"📅 Tanggal Terpilih: {selected_date_str}")
        render_cal_grid()

    def change_month(delta):
        nonlocal current_year, current_month
        current_month += delta
        if current_month > 12:
            current_month = 1
            current_year += 1
        elif current_month < 1:
            current_month = 12
            current_year -= 1
        render_cal_grid()

    render_cal_grid()
    refresh_history()


def klik_mood(parent_container=None, on_back_callback=None):
    if parent_container:
        render_mood_tracker(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("😊 Mood Tracker & Calendar - Moodiary")
        window.configure(bg=BG_PINK)
        center_window(window, 1080, 760)
        render_mood_tracker(window, None)
