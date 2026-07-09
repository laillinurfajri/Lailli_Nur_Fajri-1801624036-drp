import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


from register import buka_register




def buka_login():


    window = tk.Tk()


    window.title("Moodiary")
    window.geometry("500x650")
    window.configure(bg="#FCE4EC")
    window.resizable(False, False)


    # =====================
    # JAM REALTIME
    # =====================




    def update_jam():




        sekarang = datetime.now().strftime(
            "%d %B %Y | %H:%M:%S"
        )




        lbl_jam.config(text=sekarang)




        window.after(
            1000,
            update_jam
        )


    # =====================
    # HEADER
    # =====================


    tk.Label(
        window,
        text="🌸 MOODIARY 🌸",
        font=("Arial", 24, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(
        pady=(25, 5)
    )


    tk.Label(
        window,
        text="Your Personal Digital Journal",
        font=("Arial", 10),
        bg="#FCE4EC",
        fg="#6D4C41"
    ).pack()


    lbl_jam = tk.Label(
        window,
        bg="#FCE4EC",
        fg="#8D6E63",
        font=("Arial", 10)
    )


    lbl_jam.pack(
        pady=10
    )


    update_jam()


    # =====================
    # FORM
    # =====================


    frame = tk.Frame(
        window,
        bg="#FFF8E1",
        bd=2,
        relief="ridge"
    )


    frame.pack(
        padx=30,
        pady=20,
        fill="both"
    )


    tk.Label(
        frame,
        text="👤 Username",
        bg="#FFF8E1",
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )


    entry_username = tk.Entry(
        frame,
        font=("Arial", 11)
    )


    entry_username.pack(
        fill="x",
        padx=20
    )


    tk.Label(
        frame,
        text="🔒 Password",
        bg="#FFF8E1",
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )


    entry_password = tk.Entry(
        frame,
        show="*",
        font=("Arial", 11)
    )


    entry_password.pack(
        fill="x",
        padx=20
    )


    # =====================
    # PILIH BAHASA
    # =====================


    def pilih_bahasa():


        bahasa = tk.Toplevel()


        bahasa.title(
            "Choose Language"
        )


        bahasa.geometry("350x250")
        bahasa.configure(
            bg="#FCE4EC"
        )


        tk.Label(
            bahasa,
            text="🌍 Choose Language",
            font=("Arial", 16, "bold"),
            bg="#FCE4EC",
            fg="#AD1457"
        ).pack(
            pady=20
        )


        tk.Button(
            bahasa,
            text="🇮🇩 Bahasa Indonesia",
            width=20,
            bg="#FFF3B0",
            font=("Arial", 11, "bold")
        ).pack(
            pady=10
        )


        tk.Button(
            bahasa,
            text="🇺🇸 English",
            width=20,
            bg="#FFF3B0",
            font=("Arial", 11, "bold")
        ).pack(
            pady=10
        )


    # =====================
    # LOGIN
    # =====================


    def login():


        username = entry_username.get().strip()
        password = entry_password.get().strip()


        conn = sqlite3.connect(
            "users.db"
        )


        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            AND password=?
            """,
            (
                username,
                password
            )
        )


        data = cursor.fetchone()


        conn.close()


        if data:


            messagebox.showinfo(
                "Success",
                f"Welcome {username} 🌸"
            )


            pilih_bahasa()


        else:


            messagebox.showerror(
                "Error",
                "Username atau Password salah."
            )


    # =====================
    # BUTTON LOGIN
    # =====================


    tk.Button(
        frame,
        text="🧈 Login",
        command=login,
        bg="#FFF3B0",
        activebackground="#FFE082",
        font=("Arial", 11, "bold"),
        width=20,
        bd=0,
        cursor="hand2"
    ).pack(
        pady=(25, 10)
    )


    tk.Button(
        frame,
        text="🎀 Register",
        command=buka_register,
        bg="#F8BBD0",
        activebackground="#F48FB1",
        font=("Arial", 11, "bold"),
        width=20,
        bd=0,
        cursor="hand2"
    ).pack(
        pady=(0, 20)
    )


    # =====================
    # FOOTER
    # =====================


    tk.Label(
        window,
        text="✦ by DJL ✦",
        bg="#FCE4EC",
        fg="#9E9E9E",
        font=("Arial", 9, "italic")
    ).pack(
        side="bottom",
        pady=10
    )


    window.mainloop()
