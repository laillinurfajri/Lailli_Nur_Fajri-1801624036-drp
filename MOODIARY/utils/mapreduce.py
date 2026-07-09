# utils/mapreduce.py
import core.database as database
import sqlite3


def map_journal():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tanggal FROM journal")
    data = cursor.fetchall()
    conn.close()

    hasil_map = []
    for row in data:
        hasil_map.append((row[0], 1))
    return hasil_map


def shuffle(data_map):
    hasil = {}
    for key, value in data_map:
        if key not in hasil:
            hasil[key] = []
        hasil[key].append(value)
    return hasil


def reduce_data(data_shuffle):
    hasil_reduce = {}
    for key, values in data_shuffle.items():
        hasil_reduce[key] = sum(values)
    return hasil_reduce


def tampilkan_hasil():
    map_result = map_journal()
    print("\n=== MAP ===")
    print(map_result)

    shuffle_result = shuffle(map_result)
    print("\n=== SHUFFLE ===")
    print(shuffle_result)

    reduce_result = reduce_data(shuffle_result)
    print("\n=== REDUCE ===")
    print(reduce_result)


if __name__ == "__main__":
    tampilkan_hasil()
