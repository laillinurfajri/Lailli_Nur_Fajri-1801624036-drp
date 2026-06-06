import tkinter as tk

todo_list = []

def buka_todo():
    window = tk.Toplevel()
    window.title("To-Do List")
    window.geometry("300x400")

    def tambah_task():
        task = entry.get()

        if task:
            todo_list.append(task)
            listbox.insert(tk.END, task)
            entry.delete(0, tk.END)

    entry = tk.Entry(window)
    entry.pack(pady=10)

    tk.Button(
        window,
        text="Tambah Tugas",
        command=tambah_task
    ).pack()

    listbox = tk.Listbox(window)
    listbox.pack(
        pady=10,
        fill=tk.BOTH,
        expand=True
    )