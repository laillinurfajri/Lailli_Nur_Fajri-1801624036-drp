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


def export_user_data_to_json(filepath):
    """
    Mengekspor seluruh data akun aktif (journal, mood, todo, wish) ke file JSON.
    """
    conn = get_db_connection()
    cursor = conn.cursor()


    data = {
        "version": "2.0",
        "username": ACTIVE_USER or "Unknown",
        "journal": [],
        "mood": [],
        "todo": [],
        "wish": []
    }


    cursor.execute("SELECT id, tanggal, judul, isi, mood, kategori FROM journal")
    for row in cursor.fetchall():
        data["journal"].append({
            "id": row[0],
            "tanggal": row[1],
            "judul": row[2],
            "isi": row[3],
            "mood": row[4],
            "kategori": row[5]
        })


    cursor.execute("SELECT id, tanggal, mood, catatan FROM mood")
    for row in cursor.fetchall():
        data["mood"].append({
            "id": row[0],
            "tanggal": row[1],
            "mood": row[2],
            "catatan": row[3]
        })


    cursor.execute("SELECT id, tugas, detail, prioritas, deadline, selesai FROM todo")
    for row in cursor.fetchall():
        data["todo"].append({
            "id": row[0],
            "tugas": row[1],
            "detail": row[2],
            "prioritas": row[3],
            "deadline": row[4],
            "selesai": row[5]
        })


    cursor.execute("SELECT id, isi, kategori, biaya, prioritas, target_waktu, catatan, tercapai FROM wish")
    for row in cursor.fetchall():
        data["wish"].append({
            "id": row[0],
            "isi": row[1],
            "kategori": row[2],
            "biaya": row[3],
            "prioritas": row[4],
            "target_waktu": row[5],
            "catatan": row[6],
            "tercapai": row[7]
        })


    conn.close()


    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True




def import_user_data_from_json(filepath, replace_existing=False):
    """
    Mengimpor data dari file JSON ke dalam basis data pengguna aktif.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)


    if not isinstance(data, dict):
        raise ValueError("Format file JSON tidak valid.")


    conn = get_db_connection()
    cursor = conn.cursor()


    if replace_existing:
        cursor.execute("DELETE FROM journal")
        cursor.execute("DELETE FROM mood")
        cursor.execute("DELETE FROM todo")
        cursor.execute("DELETE FROM wish")


    # Import journal
    for item in data.get("journal", []):
        cursor.execute(
            "INSERT INTO journal (tanggal, judul, isi, mood, kategori) VALUES (?, ?, ?, ?, ?)",
            (item.get("tanggal", ""), item.get("judul", ""), item.get("isi", ""), item.get("mood", "Biasa"), item.get("kategori", "Umum"))
        )


    # Import mood
    for item in data.get("mood", []):
        cursor.execute(
            "INSERT INTO mood (tanggal, mood, catatan) VALUES (?, ?, ?)",
            (item.get("tanggal", ""), item.get("mood", "Biasa"), item.get("catatan", ""))
        )


    # Import todo
    for item in data.get("todo", []):
        cursor.execute(
            "INSERT INTO todo (tugas, detail, prioritas, deadline, selesai) VALUES (?, ?, ?, ?, ?)",
            (item.get("tugas", ""), item.get("detail", ""), item.get("prioritas", "Sedang"), item.get("deadline", ""), item.get("selesai", 0))
        )


    # Import wish
    for item in data.get("wish", []):
        cursor.execute(
            "INSERT INTO wish (isi, kategori, biaya, prioritas, target_waktu, catatan, tercapai) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (item.get("isi", ""), item.get("kategori", "Umum"), item.get("biaya", "Rp 0"), item.get("prioritas", "⭐⭐ Sedang"), item.get("target_waktu", ""), item.get("catatan", ""), item.get("tercapai", 0))
        )


    conn.commit()
    conn.close()
    return True
