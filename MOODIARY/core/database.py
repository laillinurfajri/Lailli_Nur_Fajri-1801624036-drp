import sqlite3
import os
import json

ACTIVE_USER = None


def set_active_user(username):
    global ACTIVE_USER
    ACTIVE_USER = username
    if username:
        init_user_db(username)


def rename_user_db(old_username, new_username):
    """
    Mengganti nama file database pengguna dari username lama ke username baru.
    File database lama (moodiary_<old>.db) akan di-rename menjadi
    moodiary_<new>.db sehingga seluruh data di dalamnya dipertahankan.
    """
    old_path = get_user_db_path(old_username)
    new_path = get_user_db_path(new_username)

    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)

    # Set active user ke username baru (tanpa membuat DB baru karena sudah di-rename)
    global ACTIVE_USER
    ACTIVE_USER = new_username


def get_active_user():
    return ACTIVE_USER


def get_user_db_path(username=None):
    user = username or ACTIVE_USER
    if user:
        safe_user = "".join(c for c in user if c.isalnum() or c in ('_', '-'))
        return f"moodiary_{safe_user}.db"
    return "moodiary.db"


def get_db_connection(username=None):
    db_path = get_user_db_path(username)
    return sqlite3.connect(db_path)


def init_auth_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        language TEXT DEFAULT 'ID'
    )
    """)
    conn.commit()
    conn.close()


init_db = init_auth_db


def init_user_db(username=None):
    db_path = get_user_db_path(username)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # =====================================
    # DAILY JOURNAL
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
        mood TEXT NOT NULL,
        catatan TEXT DEFAULT ''
    )
    """)

    # =====================================
    # WISH LIST
    # =====================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wish(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isi TEXT NOT NULL,
        kategori TEXT DEFAULT 'Umum',
        biaya TEXT DEFAULT 'Rp 0',
        prioritas TEXT DEFAULT '⭐⭐ Sedang',
        target_waktu TEXT DEFAULT '',
        catatan TEXT DEFAULT '',
        tercapai INTEGER DEFAULT 0
    )
    """)

    # =====================================
    # TO DO LIST
    # =====================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tugas TEXT NOT NULL,
        detail TEXT DEFAULT '',
        prioritas TEXT DEFAULT 'Medium',
        deadline TEXT DEFAULT '',
        selesai INTEGER DEFAULT 0
    )
    """)

    # =====================================
    # PROFILE
    # =====================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        bahasa TEXT DEFAULT 'ID'
    )
    """)

    conn.commit()

    migrasi = [
        "ALTER TABLE profile ADD COLUMN bahasa TEXT DEFAULT 'ID'",
        "ALTER TABLE todo ADD COLUMN detail TEXT DEFAULT ''",
        "ALTER TABLE todo ADD COLUMN prioritas TEXT DEFAULT 'Medium'",
        "ALTER TABLE todo ADD COLUMN deadline TEXT DEFAULT ''",
        "ALTER TABLE todo ADD COLUMN selesai INTEGER DEFAULT 0",
        "ALTER TABLE mood ADD COLUMN catatan TEXT DEFAULT ''",
        "ALTER TABLE wish ADD COLUMN kategori TEXT DEFAULT 'Umum'",
        "ALTER TABLE wish ADD COLUMN biaya TEXT DEFAULT 'Rp 0'",
        "ALTER TABLE wish ADD COLUMN prioritas TEXT DEFAULT '⭐⭐ Sedang'",
        "ALTER TABLE wish ADD COLUMN target_waktu TEXT DEFAULT ''",
        "ALTER TABLE wish ADD COLUMN catatan TEXT DEFAULT ''",
        "ALTER TABLE wish ADD COLUMN tercapai INTEGER DEFAULT 0"
    ]

    for sql in migrasi:
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception:
            pass

    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        nama_profil = username if username else "Pengguna"
        cursor.execute("INSERT INTO profile (nama, bahasa) VALUES (?, 'ID')", (nama_profil,))
        conn.commit()

    conn.close()


init_auth_db()
init_user_db(None)

