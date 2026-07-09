import tkinter as tk
from tkinter import messagebox
import sqlite3




def buka_register():


    window = tk.Toplevel()


    window.title("Moodiary Register")
    window.geometry("450x550")
    window.configure(bg="#FCE4EC")
    window.resizable(False, False)


    # ==========================
    # HEADER
    # ==========================


    tk.Label(
        window,
        text="🌸 MOODIARY 🌸",
        font=("Arial", 24, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(pady=(25, 5))


    tk.Label(
        window,
        text="Create Your Personal Journal Account",
        font=("Arial", 10),
        bg="#FCE4EC",
        fg="#6D4C41"
    ).pack()


    # ==========================
    # FORM FRAME
    # ==========================


    frame = tk.Frame(
        window,
        bg="#FFF8E1",
        bd=2,
        relief="ridge"
    )


    frame.pack(
        padx=25,
        pady=25,
        fill="both",
        expand=False
    )


    # Username


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


    # Password


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


    # Confirm Password


    tk.Label(
        frame,
        text="🔑 Confirm Password",
        bg="#FFF8E1",
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 5)
    )


    entry_confirm = tk.Entry(
        frame,
        show="*",
        font=("Arial", 11)
    )


    entry_confirm.pack(
        fill="x",
        padx=20
    )


    # ==========================
    # REGISTER FUNCTION
    # ==========================


    def register():


        username = entry_username.get().strip()
        password = entry_password.get().strip()
        confirm = entry_confirm.get().strip()


        if username == "" or password == "" or confirm == "":


            messagebox.showwarning(
                "Warning",
                "Please fill in all fields."
            )


            return


        if len(password) < 6:


            messagebox.showwarning(
                "Warning",
                "Password must contain at least 6 characters."
            )


            return


        if password != confirm:


            messagebox.showerror(
                "Error",
                "Password confirmation does not match."
            )


            return


        try:


            conn = sqlite3.connect(
                "moodiary.db"
            )


            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO users
                (username,password)
                VALUES (?,?)
                """,
                (
                    username,
                    password
                )
            )


            conn.commit()
            conn.close()


            messagebox.showinfo(
                "Success",
                "🎉 Account created successfully!"
            )


            window.destroy()


        except sqlite3.IntegrityError:


            messagebox.showerror(
                "Error",
                "Username already exists."
            )


    # ==========================
    # BUTTON
    # ==========================


    tk.Button(
        frame,
        text="🎀 Register",
        command=register,
        bg="#FFF3B0",
        activebackground="#FFE082",
        font=("Arial", 11, "bold"),
        width=20,
        bd=0,
        cursor="hand2"
    ).pack(
        pady=25
    )


    # ==========================
    # FOOTER
    # ==========================


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
