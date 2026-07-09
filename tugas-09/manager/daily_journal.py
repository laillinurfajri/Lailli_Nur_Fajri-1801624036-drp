import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk


import sqlite3
import json


from datetime import datetime




def klik_daily_journal():


    window = tk.Toplevel()


    window.title("📖 Daily Journal")
    window.geometry("950x750")
    window.configure(bg="#FCE4EC")


    selected_id = None


    # =====================================
    # HEADER
    # =====================================


    tk.Label(
        window,
        text="📖 Daily Journal",
        font=("Arial", 22, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(pady=10)


    tk.Label(
        window,
        text="Write your thoughts and memories today ✨",
        font=("Arial", 10),
        bg="#FCE4EC",
        fg="#6D4C41"
    ).pack()


    # =====================================
    # FORM FRAME
    # =====================================


    form_frame = tk.Frame(
        window,
        bg="#FFF8E1",
        bd=2,
        relief="ridge"
    )


    form_frame.pack(
        fill="x",
        padx=15,
        pady=10
    )


    # =====================================
    # DATE
    # =====================================


    tk.Label(
        form_frame,
        text="📅 Date",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    entry_tanggal = tk.Entry(
        form_frame,
        font=("Arial", 10)
    )


    entry_tanggal.pack(
        fill="x",
        padx=10
    )


    entry_tanggal.insert(
        0,
        datetime.now().strftime("%Y-%m-%d")
    )


    # =====================================
    # TITLE
    # =====================================


    tk.Label(
        form_frame,
        text="📝 Journal Title",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    entry_judul = tk.Entry(
        form_frame,
        font=("Arial", 10)
    )


    entry_judul.pack(
        fill="x",
        padx=10
    )


    # =====================================
    # MOOD
    # =====================================


    tk.Label(
        form_frame,
        text="😊 Today's Mood",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    mood_var = tk.StringVar()


    mood_combo = ttk.Combobox(
        form_frame,
        textvariable=mood_var,
        state="readonly"
    )


    mood_combo["values"] = (
        "😍 Very Happy",
        "😊 Happy",
        "😐 Neutral",
        "😔 Sad",
        "😭 Very Sad",
        "😡 Angry",
        "😴 Tired"
    )


    mood_combo.pack(
        fill="x",
        padx=10
    )


    mood_combo.current(1)


    # =====================================
    # CATEGORY
    # =====================================


    tk.Label(
        form_frame,
        text="🏷 Category",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    kategori_var = tk.StringVar()


    kategori_combo = ttk.Combobox(
        form_frame,
        textvariable=kategori_var,
        state="readonly"
    )


    kategori_combo["values"] = (
        "Personal",
        "College",
        "Work",
        "Goals",
        "Memories"
    )


    kategori_combo.pack(
        fill="x",
        padx=10
    )


    kategori_combo.current(0)


    # =====================================
    # JOURNAL CONTENT
    # =====================================


    tk.Label(
        form_frame,
        text="📖 Journal Content",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    txt_journal = tk.Text(
        form_frame,
        height=8,
        font=("Arial", 10)
    )


    txt_journal.pack(
        fill="x",
        padx=10,
        pady=5
    )


    # =====================================
    # CHARACTER COUNTER
    # =====================================


    char_label = tk.Label(
        form_frame,
        text="0 characters",
        bg="#FFF8E1",
        fg="#6D4C41"
    )


    char_label.pack(pady=(0, 10))


    def update_counter(event=None):


        jumlah = len(
            txt_journal.get(
                "1.0",
                tk.END
            ).strip()
        )


        char_label.config(
            text=f"{jumlah} characters"
        )


    txt_journal.bind(
        "<KeyRelease>",
        update_counter
    )


    # =====================================
    # SEARCH BOX
    # =====================================


    tk.Label(
        window,
        text="🔍 Search Journal",
        bg="#FCE4EC",
        fg="#6D4C41",
        font=("Arial", 10, "bold")
    ).pack()


    search_entry = tk.Entry(
        window,
        font=("Arial", 10)
    )


    search_entry.pack(
        fill="x",
        padx=15,
        pady=5
    )
    # =====================================
    # LISTBOX
    # =====================================


    listbox = tk.Listbox(
        window,
        font=("Arial", 10),
        height=10
    )


    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=15,
        pady=10
    )


    # =====================================
    # TAMPILKAN DATA
    # =====================================


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
        FROM journal
        ORDER BY id DESC
        """)


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | {row[4]} | {row[5]}"
            )


    # =====================================
    # SAVE JOURNAL
    # =====================================


    def tambah():


        tanggal = entry_tanggal.get().strip()
        judul = entry_judul.get().strip()


        isi = txt_journal.get(
            "1.0",
            tk.END
        ).strip()


        mood = mood_var.get()
        kategori = kategori_var.get()


        if judul == "" or isi == "":


            messagebox.showwarning(
                "Warning",
                "Please complete all fields."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO journal
        (
            tanggal,
            judul,
            isi,
            mood,
            kategori
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tanggal,
            judul,
            isi,
            mood,
            kategori
        ))


        conn.commit()
        conn.close()


        tampilkan_data()
        clear_form()


        messagebox.showinfo(
            "Success",
            "Journal saved successfully."
        )


    # =====================================
    # SELECT DATA
    # =====================================


    def pilih_data(event):


        nonlocal selected_id


        pilihan = listbox.curselection()


        if not pilihan:
            return


        data = listbox.get(
            pilihan[0]
        )


        selected_id = data.split("|")[0].strip()


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM journal
        WHERE id=?
        """,
        (
            selected_id,
        ))


        row = cursor.fetchone()


        conn.close()


        entry_tanggal.delete(
            0,
            tk.END
        )


        entry_tanggal.insert(
            0,
            row[1]
        )


        entry_judul.delete(
            0,
            tk.END
        )


        entry_judul.insert(
            0,
            row[2]
        )


        txt_journal.delete(
            "1.0",
            tk.END
        )


        txt_journal.insert(
            tk.END,
            row[3]
        )


        mood_var.set(
            row[4]
        )


        kategori_var.set(
            row[5]
        )


    # =====================================
    # UPDATE
    # =====================================


    def update():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a journal first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        UPDATE journal
        SET
            tanggal=?,
            judul=?,
            isi=?,
            mood=?,
            kategori=?
        WHERE id=?
        """,
        (
            entry_tanggal.get(),
            entry_judul.get(),
            txt_journal.get(
                "1.0",
                tk.END
            ).strip(),
            mood_var.get(),
            kategori_var.get(),
            selected_id
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        messagebox.showinfo(
            "Success",
            "Journal updated."
        )


    # =====================================
    # DELETE
    # =====================================


    def hapus():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a journal first."
            )


            return


        jawab = messagebox.askyesno(
            "Confirmation",
            "Delete this journal?"
        )


        if not jawab:
            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        DELETE FROM journal
        WHERE id=?
        """,
        (
            selected_id,
        ))


        conn.commit()
        conn.close()


        clear_form()
        tampilkan_data()


    # =====================================
    # CLEAR FORM
    # =====================================


    def clear_form():


        nonlocal selected_id


        selected_id = None


        entry_judul.delete(
            0,
            tk.END
        )


        txt_journal.delete(
            "1.0",
            tk.END
        )


        mood_combo.current(1)
        kategori_combo.current(0)


    # =====================================
    # SEARCH
    # =====================================


    def search_journal():


        keyword = search_entry.get()


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
        FROM journal
        WHERE judul LIKE ?
        OR isi LIKE ?
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        ))


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | {row[4]}"
            )


    listbox.bind(
        "<<ListboxSelect>>",
        pilih_data
    )
    # =====================================
    # LISTBOX
    # =====================================


    listbox = tk.Listbox(
        window,
        font=("Arial", 10),
        height=10
    )


    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=15,
        pady=10
    )


    # =====================================
    # TAMPILKAN DATA
    # =====================================


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
        FROM journal
        ORDER BY id DESC
        """)


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | {row[4]} | {row[5]}"
            )


    # =====================================
    # SAVE JOURNAL
    # =====================================


    def tambah():


        tanggal = entry_tanggal.get().strip()
        judul = entry_judul.get().strip()


        isi = txt_journal.get(
            "1.0",
            tk.END
        ).strip()


        mood = mood_var.get()
        kategori = kategori_var.get()


        if judul == "" or isi == "":


            messagebox.showwarning(
                "Warning",
                "Please complete all fields."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO journal
        (
            tanggal,
            judul,
            isi,
            mood,
            kategori
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tanggal,
            judul,
            isi,
            mood,
            kategori
        ))


        conn.commit()
        conn.close()


        tampilkan_data()
        clear_form()


        messagebox.showinfo(
            "Success",
            "Journal saved successfully."
        )


    # =====================================
    # SELECT DATA
    # =====================================


    def pilih_data(event):


        nonlocal selected_id


        pilihan = listbox.curselection()


        if not pilihan:
            return


        data = listbox.get(
            pilihan[0]
        )


        selected_id = data.split("|")[0].strip()


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        SELECT *
        FROM journal
        WHERE id=?
        """,
        (
            selected_id,
        ))


        row = cursor.fetchone()


        conn.close()


        entry_tanggal.delete(
            0,
            tk.END
        )


        entry_tanggal.insert(
            0,
            row[1]
        )


        entry_judul.delete(
            0,
            tk.END
        )


        entry_judul.insert(
            0,
            row[2]
        )


        txt_journal.delete(
            "1.0",
            tk.END
        )


        txt_journal.insert(
            tk.END,
            row[3]
        )


        mood_var.set(
            row[4]
        )


        kategori_var.set(
            row[5]
        )


    # =====================================
    # UPDATE
    # =====================================


    def update():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a journal first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        UPDATE journal
        SET
            tanggal=?,
            judul=?,
            isi=?,
            mood=?,
            kategori=?
        WHERE id=?
        """,
        (
            entry_tanggal.get(),
            entry_judul.get(),
            txt_journal.get(
                "1.0",
                tk.END
            ).strip(),
            mood_var.get(),
            kategori_var.get(),
            selected_id
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        messagebox.showinfo(
            "Success",
            "Journal updated."
        )


    # =====================================
    # DELETE
    # =====================================


    def hapus():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a journal first."
            )


            return


        jawab = messagebox.askyesno(
            "Confirmation",
            "Delete this journal?"
        )


        if not jawab:
            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        DELETE FROM journal
        WHERE id=?
        """,
        (
            selected_id,
        ))


        conn.commit()
        conn.close()


        clear_form()
        tampilkan_data()


    # =====================================
    # CLEAR FORM
    # =====================================


    def clear_form():


        nonlocal selected_id


        selected_id = None


        entry_judul.delete(
            0,
            tk.END
        )


        txt_journal.delete(
            "1.0",
            tk.END
        )


        mood_combo.current(1)
        kategori_combo.current(0)


    # =====================================
    # SEARCH
    # =====================================


    def search_journal():


        keyword = search_entry.get()


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
        FROM journal
        WHERE judul LIKE ?
        OR isi LIKE ?
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        ))


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | {row[4]}"
            )


    listbox.bind(
        "<<ListboxSelect>>",
        pilih_data
    )


