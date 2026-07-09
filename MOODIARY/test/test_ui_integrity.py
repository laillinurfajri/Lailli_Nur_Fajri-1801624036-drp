# tests/test_ui_integrity.py
import pytest
import sqlite3
import os
import core.database as database
import core.theme as ui_theme
import core.i18n as language


def test_theme_constants():
    assert ui_theme.BG_PINK == "#FCE4EC"
    assert ui_theme.BG_CARD_YELLOW == "#FFF8E1"
    assert ui_theme.PRIMARY_YELLOW == "#FFF3B0"
    assert ui_theme.ACCENT_PINK == "#AD1457"


def test_database_isolation(tmp_path, monkeypatch):
    test_dir = tmp_path / "testdb"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("Alice")
    assert database.get_active_user() == "Alice"
    conn_a = database.get_db_connection()
    cur_a = conn_a.cursor()
    cur_a.execute("INSERT INTO journal (tanggal, judul, isi, mood, kategori) VALUES ('2026-07-08', 'Alice Doc', 'Hello', 'Happy', 'Personal')")
    conn_a.commit()
    conn_a.close()

    database.set_active_user("Bob")
    assert database.get_active_user() == "Bob"
    conn_b = database.get_db_connection()
    cur_b = conn_b.cursor()
    cur_b.execute("SELECT COUNT(*) FROM journal")
    count_bob = cur_b.fetchone()[0]
    conn_b.close()

    assert count_bob == 0  # Alice's journal is isolated from Bob

    # Check Alice again
    database.set_active_user("Alice")
    conn_a2 = database.get_db_connection()
    cur_a2 = conn_a2.cursor()
    cur_a2.execute("SELECT COUNT(*) FROM journal")
    count_alice = cur_a2.fetchone()[0]
    conn_a2.close()

    assert count_alice == 1



def test_language_system():
    language.set_language("ID")
    assert language.get_text("journal") == "📖 Daily Journal"
    assert "Tulis refleksi harian" in language.get_text("menu_journal_desc")
    assert "Kembali ke Menu Utama" in language.get_text("back_to_main")
    assert "Pengaturan & Preferensi" in language.get_text("settings_header_title")

    language.set_language("EN")
    assert language.get_text("journal") == "📖 Daily Journal"
    assert "Write daily reflections" in language.get_text("menu_journal_desc")
    assert "Back to Main Menu" in language.get_text("back_to_main")
    assert "Settings & Preferences" in language.get_text("settings_header_title")



def test_json_export_import(tmp_path, monkeypatch):
    test_dir = tmp_path / "testdb_json"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("Charlie")
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO journal (tanggal, judul, isi, mood, kategori) VALUES ('2026-07-08', 'JSON Title', 'JSON Content', 'Gembira', 'Pribadi')")
    cur.execute("INSERT INTO todo (tugas, detail, prioritas, deadline, selesai) VALUES ('Test Task', 'Detail', 'Tinggi', '2026-07-09', 0)")
    conn.commit()
    conn.close()

    export_path = test_dir / "backup.json"
    assert database.export_user_data_to_json(str(export_path)) is True
    assert export_path.exists()

    database.set_active_user("Charlie2")
    assert database.import_user_data_from_json(str(export_path), replace_existing=True) is True

    conn2 = database.get_db_connection()
    cur2 = conn2.cursor()
    cur2.execute("SELECT judul, isi FROM journal")
    rows = cur2.fetchall()
    conn2.close()

    assert len(rows) == 1
    assert rows[0][0] == "JSON Title"
    assert rows[0][1] == "JSON Content"
