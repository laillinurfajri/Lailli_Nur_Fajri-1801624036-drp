# register.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from core.theme import BG_PINK, BG_CARD_YELLOW, BG_WHITE, ACCENT_PINK, PRIMARY_YELLOW, PRIMARY_YELLOW_HOVER, FONT_TITLE, FONT_SUBTITLE, FONT_CARD_TITLE, FONT_BODY, create_back_header


def render_register(parent_container, on_back_callback=None):
    create_back_header(
        parent_container,
        "🎀 MOODIARY REGISTER",
        "Buat akun jurnal personal baru untuk memulai catatanmu ✨",
        on_back_callback
    )

    frame = tk.Frame(
        parent_container,
        bg=BG_CARD_YELLOW,
        bd=1,
        relief="solid"
    )
    frame.pack(padx=60, pady=20, fill="x")

    tk.Label(
        frame,
        text="👤 Username Baru",
        bg=BG_CARD_YELLOW,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=24, pady=(20, 4))

    entry_username = tk.Entry(frame, font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_username.pack(fill="x", padx=24, ipady=4)

    tk.Label(
        frame,
        text="🔒 Password",
        bg=BG_CARD_YELLOW,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=24, pady=(14, 4))

    entry_password = tk.Entry(frame, show="*", font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_password.pack(fill="x", padx=24, ipady=4)

    tk.Label(
        frame,
        text="🔑 Konfirmasi Password",
        bg=BG_CARD_YELLOW,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=24, pady=(14, 4))

    entry_confirm = tk.Entry(frame, show="*", font=("Segoe UI", 10), bg=BG_WHITE, relief="solid", bd=1)
    entry_confirm.pack(fill="x", padx=24, ipady=4)

    def register():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        confirm = entry_confirm.get().strip()

        if username == "" or password == "" or confirm == "":
            messagebox.showwarning("Warning", "Harap isi seluruh kolom.")
            return

        if len(password) < 6:
            messagebox.showwarning("Warning", "Password minimal 6 karakter.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Konfirmasi password tidak cocok.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "🎉 Akun berhasil dibuat! Silakan masuk.")
            if on_back_callback:
                on_back_callback()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username sudah digunakan.")

    tk.Button(
        frame,
        text="🎀 Daftar Akun Baru",
        command=register,
        bg=PRIMARY_YELLOW,
        activebackground=PRIMARY_YELLOW_HOVER,
        font=("Segoe UI", 10, "bold"),
        bd=0,
        cursor="hand2",
        pady=8
    ).pack(fill="x", padx=24, pady=24)


def buka_register(parent_container=None, on_back_callback=None):
    if parent_container:
        render_register(parent_container, on_back_callback)
    else:
        window = tk.Toplevel()
        window.title("Moodiary Register")
        window.geometry("450x550")
        window.configure(bg="#FCE4EC")
        window.resizable(False, False)
        render_register(window, lambda: window.destroy())
