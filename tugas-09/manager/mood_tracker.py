import tkinter as tk
from tkinter import messagebox
import sqlite3


from datetime import datetime




def klik_mood():


    window = tk.Toplevel()


    window.title("😊 Mood Tracker")
    window.geometry("700x600")
    window.configure(bg="#FCE4EC")


    # =========================
    # HEADER
    # =========================


    tk.Label(
        window,
        text="😊 Mood Tracker",
        font=("Arial", 22, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(pady=10)


    tk.Label(
        window,
        text="How are you feeling today?",
        font=("Arial", 10),
        bg="#FCE4EC",
        fg="#6D4C41"
    ).pack()


    # =========================
    # FRAME
    # =========================


    frame = tk.Frame(
        window,
        bg="#FFF8E1",
        bd=2,
        relief="ridge"
    )


    frame.pack(
        fill="x",
        padx=15,
        pady=15
    )


    mood_var = tk.StringVar()


    moods = [
        "😍 Very Happy",
        "😊 Happy",
        "😐 Neutral",
        "😔 Sad",
        "😭 Very Sad",
        "😡 Angry",
        "😴 Tired",
        "🤩 Excited",
        "😎 Confident",
        "🥰 Loved"
    ]


    tk.Label(
        frame,
        text="Choose Your Mood",
        bg="#FFF8E1",
        font=("Arial", 11, "bold")
    ).pack(pady=10)


    for mood in moods:


        tk.Radiobutton(
            frame,
            text=mood,
            variable=mood_var,
            value=mood,
            bg="#FFF8E1",
            font=("Arial", 10)
        ).pack(anchor="w", padx=30)


    mood_var.set("😊 Happy")


    # =========================
    # LISTBOX
    # =========================


    listbox = tk.Listbox(
        window,
        font=("Arial", 10)
    )


    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=15,
        pady=10
    )


    # =========================
    # LOAD DATA
    # =========================


    def tampilkan_data():


        listbox.delete(
            0,
            tk.END
        )


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM mood
        ORDER BY id DESC
        """)


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[1]} | {row[2]}"
            )


    # =========================
    # SAVE MOOD
    # =========================


    def simpan_mood():


        mood = mood_var.get()


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO mood
        (
            tanggal,
            mood
        )
        VALUES (?, ?)
        """,
        (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            mood
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        messagebox.showinfo(
            "Success",
            "Mood saved successfully 😊"
        )


    # =========================
    # DELETE MOOD
    # =========================


    def hapus_terakhir():


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        DELETE FROM mood
        WHERE id = (
            SELECT MAX(id)
            FROM mood
        )
        """)


        conn.commit()
        conn.close()


        tampilkan_data()


    # =========================
    # BUTTONS
    # =========================


    tombol_frame = tk.Frame(
        window,
        bg="#FCE4EC"
    )


    tombol_frame.pack(
        pady=10
    )


    tk.Button(
        tombol_frame,
        text="💾 Save Mood",
        width=15,
        bg="#FFF3B0",
        command=simpan_mood
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="🗑 Delete Last",
        width=15,
        bg="#FFF3B0",
        command=hapus_terakhir
    ).grid(
        row=0,
        column=1,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="🔄 Refresh",
        width=15,
        bg="#FFF3B0",
        command=tampilkan_data
    ).grid(
        row=0,
        column=2,
        padx=5
    )


    tampilkan_data()
