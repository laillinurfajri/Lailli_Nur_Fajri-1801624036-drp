import tkinter as tk
from tkinter import messagebox
import sqlite3

def klik_wish_journal():


    window = tk.Toplevel()


    window.title("🌟 Wish Journal")
    window.geometry("700x600")
    window.configure(bg="#FCE4EC")


    selected_id = None


    # ==================================
    # HEADER
    # ==================================


    tk.Label(
        window,
        text="🌟 Wish Journal",
        font=("Arial", 22, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(pady=10)


    tk.Label(
        window,
        text="Write your dreams and future goals ✨",
        bg="#FCE4EC",
        fg="#6D4C41"
    ).pack()


    # ==================================
    # INPUT FRAME
    # ==================================


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


    tk.Label(
        frame,
        text="💭 My Wish",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    entry_wish = tk.Entry(
        frame,
        font=("Arial", 11)
    )


    entry_wish.pack(
        fill="x",
        padx=10,
        pady=10
    )


    # ==================================
    # LISTBOX
    # ==================================


    listbox = tk.Listbox(
        window,
        font=("Arial", 11)
    )


    listbox.pack(
        fill=tk.BOTH,
        expand=True,
        padx=15,
        pady=10
    )


    # ==================================
    # LOAD DATA
    # ==================================


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
        FROM wish
        ORDER BY id DESC
        """)


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | 🌸 {row[1]}"
            )


    # ==================================
    # PILIH DATA
    # ==================================


    def pilih_data(event):


        nonlocal selected_id


        pilihan = listbox.curselection()


        if not pilihan:
            return


        data = listbox.get(
            pilihan[0]
        )


        bagian = data.split("|")


        selected_id = bagian[0].strip()


        entry_wish.delete(
            0,
            tk.END
        )


        entry_wish.insert(
            0,
            bagian[1].replace(
                "🌸",
                ""
            ).strip()
        )


    # ==================================
    # ADD WISH
    # ==================================


    def tambah():


        wish = entry_wish.get().strip()


        if wish == "":


            messagebox.showwarning(
                "Warning",
                "Wish cannot be empty."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO wish
        (isi)
        VALUES (?)
        """,
        (
            wish,
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        entry_wish.delete(
            0,
            tk.END
        )


        messagebox.showinfo(
            "Success",
            "Wish added successfully 🌟"
        )


    # ==================================
    # UPDATE
    # ==================================


    def update():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a wish first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        UPDATE wish
        SET isi=?
        WHERE id=?
        """,
        (
            entry_wish.get(),
            selected_id
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        messagebox.showinfo(
            "Success",
            "Wish updated."
        )


    # ==================================
    # DELETE
    # ==================================


    def hapus():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a wish first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        DELETE FROM wish
        WHERE id=?
        """,
        (
            selected_id,
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        entry_wish.delete(
            0,
            tk.END
        )


        messagebox.showinfo(
            "Success",
            "Wish deleted."
        )


    # ==================================
    # CLEAR
    # ==================================


    def clear_form():


        nonlocal selected_id


        selected_id = None


        entry_wish.delete(
            0,
            tk.END
        )


    # ==================================
    # BUTTON FRAME
    # ==================================


    tombol_frame = tk.Frame(
        window,
        bg="#FCE4EC"
    )


    tombol_frame.pack(
        pady=10
    )


    tk.Button(
        tombol_frame,
        text="➕ Add",
        bg="#FFF3B0",
        width=12,
        command=tambah
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="✏ Update",
        bg="#FFF3B0",
        width=12,
        command=update
    ).grid(
        row=0,
        column=1,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="🗑 Delete",
        bg="#FFF3B0",
        width=12,
        command=hapus
    ).grid(
        row=0,
        column=2,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="🧹 Clear",
        bg="#FFF3B0",
        width=12,
        command=clear_form
    ).grid(
        row=0,
        column=3,
        padx=5
    )


    tk.Button(
        tombol_frame,
        text="🔄 Refresh",
        bg="#FFF3B0",
        width=12,
        command=tampilkan_data
    ).grid(
        row=0,
        column=4,
        padx=5
    )


    listbox.bind(
        "<<ListboxSelect>>",
        pilih_data
    )


    tampilkan_data()
