import tkinter as tk
from tkinter import messagebox
import sqlite3




def buka_todo():


    window = tk.Toplevel()


    window.title("✅ To-Do List")
    window.geometry("700x600")
    window.configure(bg="#FCE4EC")


    selected_id = None


    # ==================================
    # HEADER
    # ==================================


    tk.Label(
        window,
        text="✅ To-Do List",
        font=("Arial", 22, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(pady=10)


    tk.Label(
        window,
        text="Stay productive and achieve your goals ✨",
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
        text="📝 Task",
        bg="#FFF8E1",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))


    entry_tugas = tk.Entry(
        frame,
        font=("Arial", 11)
    )


    entry_tugas.pack(
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
        FROM todo
        ORDER BY id DESC
        """)


        data = cursor.fetchall()


        conn.close()


        for row in data:


            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]}"
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


        entry_tugas.delete(
            0,
            tk.END
        )


        entry_tugas.insert(
            0,
            bagian[1].strip()
        )


    # ==================================
    # TAMBAH
    # ==================================


    def tambah():


        tugas = entry_tugas.get().strip()


        if tugas == "":


            messagebox.showwarning(
                "Warning",
                "Task cannot be empty."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO todo
        (tugas)
        VALUES (?)
        """,
        (
            tugas,
        ))


        conn.commit()
        conn.close()


        entry_tugas.delete(
            0,
            tk.END
        )


        tampilkan_data()


    # ==================================
    # UPDATE
    # ==================================


    def update():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a task first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        UPDATE todo
        SET tugas=?
        WHERE id=?
        """,
        (
            entry_tugas.get(),
            selected_id
        ))


        conn.commit()
        conn.close()


        tampilkan_data()


        messagebox.showinfo(
            "Success",
            "Task updated."
        )


    # ==================================
    # DELETE
    # ==================================


    def hapus():


        if selected_id is None:


            messagebox.showwarning(
                "Warning",
                "Select a task first."
            )


            return


        conn = sqlite3.connect(
            "moodiary.db"
        )


        cursor = conn.cursor()


        cursor.execute("""
        DELETE FROM todo
        WHERE id=?
        """,
        (
            selected_id,
        ))


        conn.commit()
        conn.close()


        entry_tugas.delete(
            0,
            tk.END
        )


        tampilkan_data()


    # ==================================
    # CLEAR
    # ==================================


    def clear_form():


        nonlocal selected_id


        selected_id = None


        entry_tugas.delete(
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
