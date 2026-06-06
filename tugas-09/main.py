import tkinter as tk

from tools import (
    buka_todo,
    klik_mood,
    klik_daily_journal,
    klik_wish_journal,
    klik_quote
)

app = tk.Tk()
app.title("Moodiary")
app.geometry("400x500")

judul = tk.Label(
    app,
    text="Moodiary",
    font=("Arial", 20, "bold")
)

judul.pack(pady=20)

tk.Button(
    app,
    text="To-Do List",
    width=20,
    command=buka_todo
).pack(pady=10)

tk.Button(
    app,
    text="Mood Tracker",
    width=20,
    command=klik_mood
).pack(pady=10)

tk.Button(
    app,
    text="Daily Journal",
    width=20,
    command=klik_daily_journal
).pack(pady=10)

tk.Button(
    app,
    text="Wish Journal",
    width=20,
    command=klik_wish_journal
).pack(pady=10)

tk.Button(
    app,
    text="Quotes",
    width=20,
    command=klik_quote
).pack(pady=10)

app.mainloop()