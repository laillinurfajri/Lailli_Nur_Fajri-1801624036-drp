import sqlite3
from tkinter import messagebox




def tampilkan_statistik():


    conn = sqlite3.connect(
        "moodiary.db"
    )


    cursor = conn.cursor()


    cursor.execute(
        "SELECT tanggal FROM journal"
    )


    data = cursor.fetchall()


    conn.close()


    total_jurnal = len(data)


    statistik = {}


    for row in data:


        tanggal = row[0]


        if tanggal not in statistik:
            statistik[tanggal] = 0


        statistik[tanggal] += 1


    hasil = f"Total Jurnal : {total_jurnal}\n\n"


    if statistik:


        tanggal_aktif = max(
            statistik,
            key=statistik.get
        )


        hasil += (
            f"Tanggal Paling Aktif:\n"
            f"{tanggal_aktif} "
            f"({statistik[tanggal_aktif]} jurnal)\n\n"
        )


        hasil += "Rincian:\n"


        for tanggal, jumlah in statistik.items():


            hasil += (
                f"{tanggal} : "
                f"{jumlah} jurnal\n"
            )


    else:


        hasil += "Belum ada data jurnal."


    messagebox.showinfo(
        "Statistik Journal",
        hasil
    )