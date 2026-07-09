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
