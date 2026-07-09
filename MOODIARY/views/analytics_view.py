# statistik.py
# ==============================================================================
# MOODIARY - EXECUTIVE ANALYTICS DASHBOARD (SINGLE-WINDOW FRAME WITH BACK BUTTON)
# ==============================================================================
import core.database as database
import core.spark_analytics as spark_analytics
import tkinter as tk
from tkinter import ttk
import sqlite3
from collections import Counter


from core.theme import (
    BG_PINK, BG_CARD_YELLOW, BG_WHITE,
    PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER,
    SECONDARY_PINK,
    ACCENT_PINK, ACCENT_DARK,
    TEXT_DARK, TEXT_MUTED,
    BORDER_YELLOW,
    FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY, FONT_SMALL, FONT_ITALIC,
    center_window, configure_ttk_styles, create_back_header
)




def render_statistik(parent_container, on_back_callback=None):
    """
    Merender antarmuka Executive Analytics Dashboard di dalam parent_container.
    """
    configure_ttk_styles()


    # ==================================
    # HEADER DENGAN TOMBOL KEMBALI
    # ==================================
    create_back_header(
        parent_container,
        "📊 Executive Analytics Dashboard",
        "Analisis mendalam tren emosi, efektivitas tugas, dan progres pencapaian impianmu ✨",
        on_back_callback
    )


    # ==================================
    # FETCH DATA DARI DATABASE
    # ==================================
    conn = database.get_db_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT COUNT(*) FROM journal")
    total_journal = cursor.fetchone()[0]


    cursor.execute("SELECT mood FROM journal")
    mood_journal_rows = cursor.fetchall()


    cursor.execute("SELECT mood FROM mood")
    mood_tracker_rows = cursor.fetchall()


    all_moods = [m[0] for m in mood_journal_rows] + [m[0] for m in mood_tracker_rows]
    mood_counts = Counter(all_moods)
    mood_dominan = mood_counts.most_common(1)[0][0] if mood_counts else "-"


    cursor.execute("SELECT COUNT(*), SUM(selesai) FROM todo")
    row_todo = cursor.fetchone()
    total_todo = row_todo[0] or 0
    selesai_todo = row_todo[1] or 0


    cursor.execute("SELECT COUNT(*), SUM(tercapai) FROM wish")
    row_wish = cursor.fetchone()
    total_wish = row_wish[0] or 0
    tercapai_wish = row_wish[1] or 0


    conn.close()


    # ==================================
    # KPI SUMMARY CARDS (4 KARTU)
    # ==================================
    kpi_frame = tk.Frame(parent_container, bg=BG_PINK)
    kpi_frame.pack(fill="x", padx=20, pady=4)


    for i in range(4):
        kpi_frame.columnconfigure(i, weight=1)


    def buat_kpi_card(parent, col, ikon, judul, nilai, subteks):
        card = tk.Frame(
            parent,
            bg=BG_CARD_YELLOW,
            bd=1,
            relief="solid"
        )
        card.grid(row=0, column=col, padx=6, pady=2, sticky="nsew")


        content = tk.Frame(card, bg=BG_CARD_YELLOW)
        content.pack(fill="both", expand=True, padx=14, pady=10)


        top_bar = tk.Frame(content, bg=BG_CARD_YELLOW)
        top_bar.pack(fill="x")


        tk.Label(top_bar, text=ikon, font=("Segoe UI", 18), bg=BG_CARD_YELLOW).pack(side="left")
        tk.Label(top_bar, text=judul, font=("Segoe UI", 9, "bold"), bg=BG_CARD_YELLOW, fg=TEXT_MUTED).pack(side="right")


        tk.Label(
            content,
            text=str(nilai),
            font=("Segoe UI", 18, "bold"),
            bg=BG_CARD_YELLOW,
            fg=ACCENT_PINK
        ).pack(anchor="w", pady=(6, 2))


        tk.Label(
            content,
            text=subteks,
            font=FONT_SMALL,
            bg=BG_CARD_YELLOW,
            fg=TEXT_DARK
        ).pack(anchor="w")


    buat_kpi_card(
        kpi_frame, 0, "📖", "CATATAN JURNAL", total_journal,
        "Total catatan tersimpan"
    )


    p_todo = int((selesai_todo / total_todo * 100)) if total_todo > 0 else 0
    buat_kpi_card(
        kpi_frame, 1, "✅", "TUGAS SELESAI", f"{selesai_todo} / {total_todo}",
        f"Progres produktivitas: {p_todo}%"
    )


    p_wish = int((tercapai_wish / total_wish * 100)) if total_wish > 0 else 0
    buat_kpi_card(
        kpi_frame, 2, "🌟", "WISH TERCAPAI", f"{tercapai_wish} / {total_wish}",
        f"Rasio pencapaian: {p_wish}%"
    )


    buat_kpi_card(
        kpi_frame, 3, "😊", "MOOD DOMINAN", mood_dominan,
        "Emosi paling sering muncul"
    )


    # ==================================
    # NOTEBOOK (TABBED CHARTS)
    # ==================================
    notebook = ttk.Notebook(parent_container)
    notebook.pack(fill="both", expand=True, padx=20, pady=(6, 16))


    # --- TAB 1: MOOD ANALYTICS ---
    tab_mood = tk.Frame(notebook, bg=BG_CARD_YELLOW)
    notebook.add(tab_mood, text="   😊 Tren & Grafik Suasana Hati   ")


    mood_chart_frame = tk.Frame(tab_mood, bg=BG_CARD_YELLOW)
    mood_chart_frame.pack(fill="both", expand=True, padx=18, pady=14)


    tk.Label(
        mood_chart_frame,
        text="📈 Distribusi Suasana Hati (Berdasarkan Seluruh Catatan Jurnal & Tracker)",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(0, 8))


    canvas_mood = tk.Canvas(
        mood_chart_frame,
        bg=BG_WHITE,
        height=320,
        highlightbackground=BORDER_YELLOW,
        highlightthickness=1
    )
    canvas_mood.pack(fill="both", expand=True)


    def draw_mood_chart():
        canvas_mood.delete("all")
        width = canvas_mood.winfo_width()
        height = canvas_mood.winfo_height()
        if width < 100:
            width = 980
            height = 320


        if not mood_counts:
            canvas_mood.create_text(
                width / 2, height / 2,
                text="Belum ada data suasana hati tercatat.",
                font=FONT_CARD_TITLE,
                fill=TEXT_MUTED
            )
            return


        items = list(mood_counts.items())
        max_val = max([v for k, v in items]) if items else 1
        num_bars = len(items)
        margin_left = 60
        margin_bottom = 50
        chart_w = width - margin_left - 40
        chart_h = height - margin_bottom - 40


        for idx in range(5):
            y = 30 + (chart_h / 4) * idx
            val_label = int(max_val * (4 - idx) / 4)
            canvas_mood.create_line(margin_left, y, margin_left + chart_w, y, fill="#E0E0E0", dash=(2, 2))
            canvas_mood.create_text(margin_left - 15, y, text=str(val_label), font=FONT_SMALL, fill=TEXT_MUTED)


        base_y = height - margin_bottom
        canvas_mood.create_line(margin_left, base_y, margin_left + chart_w, base_y, fill=TEXT_DARK, width=2)


        bar_w = min(65, chart_w / (num_bars * 1.6))
        spacing = (chart_w - (num_bars * bar_w)) / (num_bars + 1)


        colors = ["#F06292", "#BA68C8", "#4FC3F7", "#81C784", "#FFD54F", "#FF8A65", "#A1887F"]


        for i, (mood_name, count) in enumerate(items):
            x1 = margin_left + spacing + i * (bar_w + spacing)
            x2 = x1 + bar_w
            bar_h = (count / max_val) * chart_h
            y1 = base_y - bar_h
            y2 = base_y


            c = colors[i % len(colors)]
            canvas_mood.create_rectangle(x1, y1, x2, y2, fill=c, outline=ACCENT_DARK, width=1)
            canvas_mood.create_text((x1 + x2) / 2, y1 - 12, text=str(count), font=("Segoe UI", 9, "bold"), fill=ACCENT_DARK)
            canvas_mood.create_text((x1 + x2) / 2, base_y + 16, text=mood_name[:12], font=FONT_SMALL, fill=TEXT_DARK)


    canvas_mood.bind("<Configure>", lambda e: draw_mood_chart())


    # --- TAB 2: PRODUCTIVITY ANALYTICS ---
    tab_todo = tk.Frame(notebook, bg=BG_CARD_YELLOW)
    notebook.add(tab_todo, text="   ✅ Analisis Produktivitas Tugas   ")


    todo_content = tk.Frame(tab_todo, bg=BG_CARD_YELLOW)
    todo_content.pack(fill="both", expand=True, padx=20, pady=16)


    tk.Label(
        todo_content,
        text="📈 Efektivitas Penyelesaian Tugas",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(0, 6))


    progress_bar_frame = tk.Frame(todo_content, bg=BG_WHITE, bd=1, relief="solid")
    progress_bar_frame.pack(fill="x", pady=(0, 16))


    canvas_todo_bar = tk.Canvas(progress_bar_frame, height=45, bg=BG_WHITE, highlightthickness=0)
    canvas_todo_bar.pack(fill="x", padx=10, pady=10)


    def draw_todo_bar():
        canvas_todo_bar.delete("all")
        w = canvas_todo_bar.winfo_width()
        if w < 100:
            w = 940
        h = 45
        canvas_todo_bar.create_rectangle(0, 0, w, h, fill="#EEEEEE", outline="#BDBDBD")


        if total_todo > 0:
            p = selesai_todo / total_todo
            w_fill = w * p
            canvas_todo_bar.create_rectangle(0, 0, w_fill, h, fill="#A5D6A7", outline="#388E3C")
            canvas_todo_bar.create_text(
                w / 2, h / 2,
                text=f"Progres Penyelesaian Tugas: {int(p * 100)}% ({selesai_todo} dari {total_todo} Selesai)",
                font=("Segoe UI", 11, "bold"),
                fill=TEXT_DARK
            )
        else:
            canvas_todo_bar.create_text(
                w / 2, h / 2,
                text="Belum ada data tugas pada To-Do List.",
                font=FONT_CARD_TITLE,
                fill=TEXT_MUTED
            )


    canvas_todo_bar.bind("<Configure>", lambda e: draw_todo_bar())


    tk.Label(
        todo_content,
        text="🔥 Distribusi Prioritas Tugas",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(4, 6))


    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prioritas, COUNT(*) FROM todo GROUP BY prioritas")
    prio_rows = cursor.fetchall()
    conn.close()


    prio_card = tk.Frame(todo_content, bg=BG_WHITE, bd=1, relief="solid")
    prio_card.pack(fill="both", expand=True)


    canvas_prio = tk.Canvas(prio_card, bg=BG_WHITE, highlightthickness=0)
    canvas_prio.pack(fill="both", expand=True, padx=16, pady=16)


    def draw_prio_chart():
        canvas_prio.delete("all")
        w = canvas_prio.winfo_width()
        h = canvas_prio.winfo_height()
        if w < 100:
            w = 940
            h = 200


        if not prio_rows:
            canvas_prio.create_text(w / 2, h / 2, text="Belum ada tugas berprioritas.", font=FONT_CARD_TITLE, fill=TEXT_MUTED)
            return


        max_val = max([count for _, count in prio_rows]) or 1
        num_bars = len(prio_rows)
        bar_w = min(100, (w - 120) / (num_bars * 1.8))
        spacing = (w - 120 - (num_bars * bar_w)) / (num_bars + 1)
        base_y = h - 40


        canvas_prio.create_line(60, base_y, w - 60, base_y, fill=TEXT_DARK, width=2)


        for idx, (prio_name, count) in enumerate(prio_rows):
            x1 = 60 + spacing + idx * (bar_w + spacing)
            x2 = x1 + bar_w
            bar_h = (count / max_val) * (h - 80)
            y1 = base_y - bar_h


            warna = "#EF9A9A" if "High" in (prio_name or "") else ("#FFF59D" if "Medium" in (prio_name or "") else "#A5D6A7")
            canvas_prio.create_rectangle(x1, y1, x2, base_y, fill=warna, outline=TEXT_DARK)
            canvas_prio.create_text((x1 + x2) / 2, y1 - 14, text=str(count), font=("Segoe UI", 9, "bold"), fill=ACCENT_DARK)
            canvas_prio.create_text((x1 + x2) / 2, base_y + 16, text=(prio_name or "Umum"), font=FONT_SMALL, fill=TEXT_DARK)


    canvas_prio.bind("<Configure>", lambda e: draw_prio_chart())


    # --- TAB 3: WISH LIST ANALYTICS ---
    tab_wish = tk.Frame(notebook, bg=BG_CARD_YELLOW)
    notebook.add(tab_wish, text="   🌟 Pencapaian Impian (Wish List)   ")


    wish_content = tk.Frame(tab_wish, bg=BG_CARD_YELLOW)
    wish_content.pack(fill="both", expand=True, padx=20, pady=16)


    tk.Label(
        wish_content,
        text="🌟 Progres Pencapaian Impian & Masa Depan",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(0, 6))


    wish_progress_frame = tk.Frame(wish_content, bg=BG_WHITE, bd=1, relief="solid")
    wish_progress_frame.pack(fill="x", pady=(0, 16))


    canvas_wish_bar = tk.Canvas(wish_progress_frame, height=45, bg=BG_WHITE, highlightthickness=0)
    canvas_wish_bar.pack(fill="x", padx=10, pady=10)


    def draw_wish_bar():
        canvas_wish_bar.delete("all")
        w = canvas_wish_bar.winfo_width()
        if w < 100:
            w = 940
        h = 45
        canvas_wish_bar.create_rectangle(0, 0, w, h, fill="#EEEEEE", outline="#BDBDBD")


        if total_wish > 0:
            p = tercapai_wish / total_wish
            w_fill = w * p
            canvas_wish_bar.create_rectangle(0, 0, w_fill, h, fill="#FFE082", outline="#FBC02D")
            canvas_wish_bar.create_text(
                w / 2, h / 2,
                text=f"Rasio Impian Tercapai: {int(p * 100)}% ({tercapai_wish} dari {total_wish} Impian)",
                font=("Segoe UI", 11, "bold"),
                fill=TEXT_DARK
            )
        else:
            canvas_wish_bar.create_text(
                w / 2, h / 2,
                text="Belum ada impian tercatat pada Wish List.",
                font=FONT_CARD_TITLE,
                fill=TEXT_MUTED
            )


    canvas_wish_bar.bind("<Configure>", lambda e: draw_wish_bar())


    tk.Label(
        wish_content,
        text="🏷️ Distribusi Kategori Impian",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(anchor="w", pady=(4, 6))


    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kategori, COUNT(*) FROM wish GROUP BY kategori")
    wish_cat_rows = cursor.fetchall()
    conn.close()


    cat_card = tk.Frame(wish_content, bg=BG_WHITE, bd=1, relief="solid")
    cat_card.pack(fill="both", expand=True)


    canvas_wish_cat = tk.Canvas(cat_card, bg=BG_WHITE, highlightthickness=0)
    canvas_wish_cat.pack(fill="both", expand=True, padx=16, pady=16)


    def draw_wish_cat():
        canvas_wish_cat.delete("all")
        w = canvas_wish_cat.winfo_width()
        h = canvas_wish_cat.winfo_height()
        if w < 100:
            w = 940
            h = 200


        if not wish_cat_rows:
            canvas_wish_cat.create_text(w / 2, h / 2, text="Belum ada data kategori impian.", font=FONT_CARD_TITLE, fill=TEXT_MUTED)
            return


        max_val = max([c for _, c in wish_cat_rows]) or 1
        num_bars = len(wish_cat_rows)
        bar_w = min(80, (w - 100) / (num_bars * 1.6))
        spacing = (w - 100 - (num_bars * bar_w)) / (num_bars + 1)
        base_y = h - 40


        canvas_wish_cat.create_line(50, base_y, w - 50, base_y, fill=TEXT_DARK, width=2)
        colors = ["#CE93D8", "#F48FB1", "#80DEEA", "#FFF59D", "#A5D6A7", "#FFAB91"]


        for idx, (cat_name, count) in enumerate(wish_cat_rows):
            x1 = 50 + spacing + idx * (bar_w + spacing)
            x2 = x1 + bar_w
            bar_h = (count / max_val) * (h - 80)
            y1 = base_y - bar_h


            c = colors[idx % len(colors)]
            canvas_wish_cat.create_rectangle(x1, y1, x2, base_y, fill=c, outline=TEXT_DARK)
            canvas_wish_cat.create_text((x1 + x2) / 2, y1 - 14, text=str(count), font=("Segoe UI", 9, "bold"), fill=ACCENT_DARK)
            canvas_wish_cat.create_text((x1 + x2) / 2, base_y + 16, text=(cat_name or "Umum")[:10], font=FONT_SMALL, fill=TEXT_DARK)


    canvas_wish_cat.bind("<Configure>", lambda e: draw_wish_cat())


    # --- TAB 4: APACHE PYSPARK BIG DATA ANALYTICS (MAPREDUCE 2 NODE) ---
    tab_spark = tk.Frame(notebook, bg=BG_CARD_YELLOW)
    notebook.add(tab_spark, text="   \u26a1 PySpark MapReduce (2 Node)   ")


    spark_content = tk.Frame(tab_spark, bg=BG_CARD_YELLOW)
    spark_content.pack(fill="both", expand=True, padx=20, pady=14)


    # Header & Status Engine
    spark_header = tk.Frame(spark_content, bg=BG_CARD_YELLOW)
    spark_header.pack(fill="x", pady=(0, 8))


    tk.Label(
        spark_header,
        text="\u26a1 PySpark MapReduce Engine (2 Node/Partisi)",
        font=FONT_CARD_TITLE,
        bg=BG_CARD_YELLOW,
        fg=ACCENT_PINK
    ).pack(side="left")


    engine_status_label = tk.Label(
        spark_header,
        text="",
        font=("Segoe UI", 8, "italic"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_MUTED
    )
    engine_status_label.pack(side="right")


    # Tombol Aksi (Generate Dummy + Jalankan MapReduce)
    btn_frame = tk.Frame(spark_content, bg=BG_CARD_YELLOW)
    btn_frame.pack(fill="x", pady=(0, 10))


    from tkinter import messagebox as spark_msgbox


    def generate_dummy():
        konfirmasi = spark_msgbox.askyesno(
            "Generate Data Dummy",
            "Apakah Anda ingin membuat 50 catatan jurnal, 20 tugas, dan 30 mood tracker dummy?\n\n"
            "Data ini akan mensimulasikan dataset besar (Big Data) untuk diproses oleh MapReduce PySpark."
        )
        if konfirmasi:
            result = spark_analytics.generate_dummy_data(
                jumlah_journal=50, jumlah_todo=20, jumlah_mood=30
            )
            spark_msgbox.showinfo(
                "Data Dummy Berhasil Dibuat",
                f"\U0001f389 Total {result['total_records']} record dummy berhasil dibuat!\n\n"
                f"  \u2022 Jurnal  : {result['journal_created']} catatan\n"
                f"  \u2022 To-Do   : {result['todo_created']} tugas\n"
                f"  \u2022 Mood    : {result['mood_created']} entri\n\n"
                f"Tekan tombol '\U0001f680 Jalankan MapReduce' untuk memproses data."
            )


    tk.Button(
        btn_frame,
        text="\U0001f4e6 Generate Data Dummy (Big Data Simulation)",
        command=generate_dummy,
        bg="#E1BEE7",
        activebackground="#CE93D8",
        font=("Segoe UI", 9, "bold"),
        fg=TEXT_DARK,
        bd=1,
        relief="solid",
        cursor="hand2",
        padx=14,
        pady=7
    ).pack(side="left", padx=(0, 10))


    def jalankan_analisis_spark():
        engine_status_label.config(text="\u23f3 Memproses MapReduce 2 Node...", fg="#FF6F00")
        tab_spark.update_idletasks()


        report = spark_analytics.get_analytics_report()


        if report["pyspark_available"]:
            engine_status_label.config(text="\u2705 Engine: Apache PySpark MapReduce", fg="#2E7D32")
        else:
            engine_status_label.config(text="\U0001f504 Engine: Python Fallback MapReduce", fg="#E65100")


        draw_word_freq_chart(report["word_frequency"])
        canvas_wf.bind("<Configure>", lambda e: draw_word_freq_chart(report["word_frequency"]))
        update_stats_text(report)


    tk.Button(
        btn_frame,
        text="\U0001f680 Jalankan MapReduce PySpark (2 Node)",
        command=jalankan_analisis_spark,
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 10, "bold"),
        fg=ACCENT_PINK,
        bd=1,
        relief="solid",
        cursor="hand2",
        padx=14,
        pady=7
    ).pack(side="left")


    # Area hasil analisis (2 kolom)
    result_area = tk.Frame(spark_content, bg=BG_CARD_YELLOW)
    result_area.pack(fill="both", expand=True, pady=(0, 6))


    col_left = tk.Frame(result_area, bg=BG_CARD_YELLOW)
    col_left.pack(side="left", fill="both", expand=True, padx=(0, 10))


    col_right = tk.Frame(result_area, bg=BG_CARD_YELLOW)
    col_right.pack(side="left", fill="both", expand=True, padx=(10, 0))


    # Kolom Kiri: Top 10 Kata Kunci (Word Frequency dari MapReduce)
    tk.Label(
        col_left,
        text="\U0001f522 Top Kata Kunci - MapReduce Word Count",
        font=("Segoe UI", 10, "bold"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", pady=(0, 6))


    canvas_wf = tk.Canvas(
        col_left, bg=BG_WHITE, height=240,
        highlightbackground=BORDER_YELLOW, highlightthickness=1
    )
    canvas_wf.pack(fill="both", expand=True)


    # Kolom Kanan: Statistik MapReduce & Partisi
    tk.Label(
        col_right,
        text="\U0001f4ca Laporan MapReduce & Partisi Node",
        font=("Segoe UI", 10, "bold"),
        bg=BG_CARD_YELLOW,
        fg=TEXT_DARK
    ).pack(anchor="w", pady=(0, 6))


    stats_frame = tk.Frame(
        col_right, bg=BG_WHITE, bd=1, relief="solid",
        highlightbackground=BORDER_YELLOW, highlightthickness=1
    )
    stats_frame.pack(fill="both", expand=True)


    stats_text = tk.Text(
        stats_frame, font=("Consolas", 9), bg=BG_WHITE, fg=TEXT_DARK,
        wrap="word", bd=0, state="disabled", padx=14, pady=14
    )
    stats_text.pack(fill="both", expand=True)


    def draw_word_freq_chart(word_freq):
        canvas_wf.delete("all")
        w = canvas_wf.winfo_width()
        h = canvas_wf.winfo_height()
        if w < 100:
            w, h = 460, 240


        if not word_freq:
            canvas_wf.create_text(
                w / 2, h / 2,
                text="Tekan tombol MapReduce untuk memulai analisis.",
                font=FONT_CARD_TITLE, fill=TEXT_MUTED
            )
            return


        max_val = word_freq[0][1] if word_freq else 1
        margin_left = 110
        margin_top = 16
        bar_h = max(16, (h - margin_top * 2) / len(word_freq) - 6)
        colors = ["#F06292", "#BA68C8", "#4FC3F7", "#81C784", "#FFD54F",
                  "#FF8A65", "#A1887F", "#90A4AE", "#CE93D8", "#80CBC4"]


        for i, (word, count) in enumerate(word_freq):
            y1 = margin_top + i * (bar_h + 6)
            y2 = y1 + bar_h
            bar_w = ((w - margin_left - 60) * count / max_val)
            c = colors[i % len(colors)]


            canvas_wf.create_text(
                margin_left - 8, (y1 + y2) / 2,
                text=word[:14], font=("Segoe UI", 9), fill=TEXT_DARK, anchor="e"
            )
            canvas_wf.create_rectangle(
                margin_left, y1, margin_left + bar_w, y2,
                fill=c, outline=ACCENT_DARK, width=1
            )
            canvas_wf.create_text(
                margin_left + bar_w + 8, (y1 + y2) / 2,
                text=str(count), font=("Segoe UI", 9, "bold"),
                fill=ACCENT_DARK, anchor="w"
            )


    def update_stats_text(report):
        stats_text.config(state="normal")
        stats_text.delete("1.0", tk.END)


        p_sizes = report.get("partition_sizes", [0, 0])
        n_parts = report.get("num_partitions", 2)


        lines = [
            "\u2550" * 40,
            "  PYSPARK MAPREDUCE ANALYTICS REPORT",
            "\u2550" * 40,
            "",
            f"  Engine : {report['engine']}",
            "",
            "\u2500" * 40,
            "  KONFIGURASI MAPREDUCE",
            "\u2500" * 40,
            f"  Jumlah Node/Partisi  : {n_parts}",
        ]
        for idx, size in enumerate(p_sizes):
            lines.append(f"  Node {idx+1} (Partisi {idx})  : {size} record")
        lines.append(f"  Total Data Dipecah   : {sum(p_sizes)} record")
        lines.append("")
        lines.append("\u2500" * 40)
        lines.append("  HASIL PEMROSESAN")
        lines.append("\u2500" * 40)
        lines.append(f"  Jurnal Diproses      : {report['total_journal_processed']}")
        lines.append(f"  Tugas Diproses       : {report['total_todo_processed']}")
        lines.append(f"  Tingkat Penyelesaian  : {report['todo_completion_rate']}%")
        lines.append("")
        lines.append("\u2500" * 40)
        lines.append("  DISTRIBUSI MOOD (Reduce Result)")
        lines.append("\u2500" * 40)


        for mood, count in report.get("mood_distribution", []):
            bar = "\u2588" * min(count, 20)
            lines.append(f"  {mood:<16} {bar} {count}")


        if not report.get("mood_distribution"):
            lines.append("  (Belum ada data mood)")


        lines.append("")
        lines.append("\u2550" * 40)


        stats_text.insert(tk.END, "\n".join(lines))
        stats_text.config(state="disabled")






def tampilkan_statistik(parent_container=None, on_back_callback=None):
    if parent_container:
        render_statistik(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("📊 Executive Analytics Dashboard - Moodiary")
        window.configure(bg=BG_PINK)
        center_window(window, 1080, 760)
        render_statistik(window, None)
