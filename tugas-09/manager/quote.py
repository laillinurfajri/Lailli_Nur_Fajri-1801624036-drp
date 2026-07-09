import tkinter as tk
import random


from language import LANG, QUOTES




def klik_quote():


    quote = random.choice(
        QUOTES[LANG]
    )


    if LANG == "ID":
        judul = "💬 Kutipan Hari Ini 💬"
    else:
        judul = "💬 Quote of The Day 💬"


    window = tk.Toplevel()


    window.title("Moodiary Quotes")
    window.geometry("550x350")
    window.configure(bg="#FCE4EC")


    tk.Label(
        window,
        text=judul,
        font=("Arial", 18, "bold"),
        bg="#FCE4EC",
        fg="#AD1457"
    ).pack(
        pady=20
    )


    frame = tk.Frame(
        window,
        bg="#FFF8E1",
        bd=2,
        relief="ridge"
    )


    frame.pack(
        padx=25,
        pady=10,
        fill="both",
        expand=True
    )


    tk.Label(
        frame,
        text=quote,
        font=("Arial", 14, "italic"),
        wraplength=420,
        justify="center",
        bg="#FFF8E1",
        fg="#6D4C41"
    ).pack(
        expand=True,
        padx=20,
        pady=20
    )


    if LANG == "ID":
        teks_tombol = "🎲 Kutipan Lain"
    else:
        teks_tombol = "🎲 New Quote"


    def quote_baru():


        quote_label.config(
            text=random.choice(
                QUOTES[LANG]
            )
        )


    quote_label = tk.Label(
        frame,
        text=quote,
        font=("Arial", 14, "italic"),
        wraplength=420,
        justify="center",
        bg="#FFF8E1",
        fg="#6D4C41"
    )


    quote_label.pack(
        expand=True,
        padx=20,
        pady=20
    )


    tk.Button(
        window,
        text=teks_tombol,
        command=quote_baru,
        bg="#FFF3B0",
        activebackground="#FFE082",
        font=("Arial", 10, "bold"),
        bd=0,
        width=18,
        cursor="hand2"
    ).pack(
        pady=15
    )


    tk.Label(
        window,
        text="✦ Moodiary by DJL ✦",
        bg="#FCE4EC",
        fg="#9E9E9E",
        font=("Arial", 9, "italic")
    ).pack(
        side="bottom",
        pady=8
    )