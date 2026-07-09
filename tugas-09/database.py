import sqlite3




def create_database():


    conn = sqlite3.connect("moodiary.db")
    cursor = conn.cursor()


    # =====================================
    # USER ACCOUNT
    # =====================================


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        language TEXT DEFAULT 'ID'
    )
    """)


    # =====================================
    # DAILY JOURNAL PREMIUM
    # =====================================


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        judul TEXT NOT NULL,
        isi TEXT NOT NULL,
        mood TEXT,
        kategori TEXT
    )
    """)


    # =====================================
    # MOOD TRACKER
    # =====================================


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        mood TEXT NOT NULL
    )
    """)


    # =====================================
    # WISH JOURNAL
    # =====================================


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wish(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isi TEXT NOT NULL
    )
    """)


    # =====================================
    # TO DO LIST
    # =====================================


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tugas TEXT NOT NULL
    )
    """)


    conn.commit()
    conn.close()




create_database()
