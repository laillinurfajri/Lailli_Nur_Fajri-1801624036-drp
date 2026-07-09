import tkinter as tk
from datetime import datetime
import database


from tools import (
    buka_todo,
    klik_mood,
    klik_daily_journal,
    klik_wish_journal,
    klik_quote,
    tampilkan_statistik
)


app = tk.Tk()


app.title("Moodiary")
app.geometry("500x750")
app.configure(bg="#FCE4EC")
app.resizable(False, False)


# ==================================
# JAM REALTIME
# ==================================


def update_waktu():


    sekarang = datetime.now()


    tanggal = sekarang.strftime(
        "%A, %d %B %Y"
    )


    jam = sekarang.strftime(
        "%H:%M:%S"
    )


    lbl_tanggal.config(
        text=tanggal
    )


    lbl_jam.config(
        text=jam
    )


    app.after(
        1000,
        update_waktu
    )


# ==================================
# HEADER
# ==================================


tk.Label(
    app,
    text="🌸 MOODIARY 🌸",
    font=("Arial", 24, "bold"),
    bg="#FCE4EC",
    fg="#AD1457"
).pack(
    pady=(25, 5)
)


tk.Label(
    app,
    text="Welcome to Moodiary",
    font=("Arial", 12),
    bg="#FCE4EC",
    fg="#6D4C41"
).pack()


lbl_tanggal = tk.Label(
    app,
    bg="#FCE4EC",
    fg="#8D6E63",
    font=("Arial", 10)
)


lbl_tanggal.pack()


lbl_jam = tk.Label(
    app,
    bg="#FCE4EC",
    fg="#8D6E63",
    font=("Arial", 14, "bold")
)


lbl_jam.pack(
    pady=(0, 15)
)


update_waktu()


# ==================================
# QUOTE HARIAN
# ==================================


quote_box = tk.Label(
    app,
    text="✨ Small progress is still progress ✨",
    bg="#FFF8E1",
    fg="#6D4C41",
    font=("Arial", 10, "italic"),
    wraplength=350,
    relief="ridge",
    padx=15,
    pady=10
)


quote_box.pack(
    padx=25,
    pady=10,
    fill="x"
)


# ==================================
# MENU FRAME
# ==================================


menu_frame = tk.Frame(
    app,
    bg="#FCE4EC"
)


menu_frame.pack(
    pady=20
)


# ==================================
# BUTTON STYLE
# ==================================


button_style = {
    "width": 25,
    "height": 2,
    "bg": "#FFF3B0",
    "activebackground": "#FFE082",
    "font": ("Arial", 11, "bold"),
    "bd": 0,
    "cursor": "hand2"
}


# ==================================
# BUTTON MENU
# ==================================


tk.Button(
    menu_frame,
    text="📖 Daily Journal",
    command=klik_daily_journal,
    **button_style
).pack(
    pady=8
)


tk.Button(
    menu_frame,
    text="😊 Mood Tracker",
    command=klik_mood,
    **button_style
).pack(
    pady=8
)


tk.Button(
    menu_frame,
    text="🌟 Wish Journal",
    command=klik_wish_journal,
    **button_style
).pack(
    pady=8
)


tk.Button(
    menu_frame,
    text="📝 To Do List",
    command=buka_todo,
    **button_style
).pack(
    pady=8
)


tk.Button(
    menu_frame,
    text="💬 Quotes",
    command=klik_quote,
    **button_style
).pack(
    pady=8
)


tk.Button(
    menu_frame,
    text="📊 Statistik Journal",
    command=tampilkan_statistik,
    **button_style
).pack(
    pady=8
)


# ==================================
# FOOTER
# ==================================


footer = tk.Label(
    app,
    text="✦ by DJL ✦",
    bg="#FCE4EC",
    fg="#9E9E9E",
    font=("Arial", 9, "italic")
)


footer.pack(
    side="bottom",
    pady=10
)


app.mainloop()