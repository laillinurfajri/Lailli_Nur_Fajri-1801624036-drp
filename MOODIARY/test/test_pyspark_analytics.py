# tests/test_pyspark_analytics.py
# ==============================================================================
# MOODIARY - AUTOMATED TESTS FOR PYSPARK MAPREDUCE ANALYTICS MODULE
# ==============================================================================
import pytest
import core.database as database
import core.spark_analytics as spark_analytics


def test_generate_dummy_data(tmp_path, monkeypatch):
    """
    Pastikan fungsi generate_dummy_data() membuat data dummy dengan jumlah
    yang benar ke dalam database SQLite pengguna aktif.
    """
    test_dir = tmp_path / "testdb_dummy"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("DummyUser")
    result = spark_analytics.generate_dummy_data(
        jumlah_journal=10, jumlah_todo=5, jumlah_mood=8
    )

    assert result["journal_created"] == 10
    assert result["todo_created"] == 5
    assert result["mood_created"] == 8
    assert result["total_records"] == 23

    # Verifikasi data benar-benar tersimpan di SQLite
    conn = database.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM journal")
    assert cur.fetchone()[0] == 10
    cur.execute("SELECT COUNT(*) FROM todo")
    assert cur.fetchone()[0] == 5
    cur.execute("SELECT COUNT(*) FROM mood")
    assert cur.fetchone()[0] == 8
    conn.close()


def test_mapreduce_report_has_partition_info(tmp_path, monkeypatch):
    """
    Pastikan laporan MapReduce memiliki informasi partisi/node
    yang menunjukkan data dipecah ke minimal 2 bagian.
    """
    test_dir = tmp_path / "testdb_mapreduce"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("MapReduceUser")
    spark_analytics.generate_dummy_data(jumlah_journal=20, jumlah_todo=6, jumlah_mood=10)

    report = spark_analytics.get_analytics_report()

    # Harus ada info partisi
    assert "num_partitions" in report
    assert "partition_sizes" in report
    assert report["num_partitions"] == 2
    assert len(report["partition_sizes"]) == 2

    # Jumlah data di kedua partisi harus sama dengan total jurnal
    assert sum(report["partition_sizes"]) == report["total_journal_processed"]

    # Kedua partisi harus memiliki data (tidak boleh ada yang kosong)
    for size in report["partition_sizes"]:
        assert size > 0


def test_mapreduce_word_frequency_with_dummy(tmp_path, monkeypatch):
    """
    Pastikan proses MapReduce Word Count menghasilkan kata kunci
    bermakna dari data dummy (bukan stop words).
    """
    test_dir = tmp_path / "testdb_mapreduce_wf"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("WFUser")
    spark_analytics.generate_dummy_data(jumlah_journal=30, jumlah_todo=5, jumlah_mood=5)

    report = spark_analytics.get_analytics_report()

    assert len(report["word_frequency"]) > 0

    found_words = [word for word, count in report["word_frequency"]]

    # Stop words tidak boleh muncul di hasil
    for stop_word in ["yang", "dan", "dari", "untuk", "dengan", "adalah"]:
        assert stop_word not in found_words


def test_mapreduce_mood_distribution(tmp_path, monkeypatch):
    """
    Pastikan proses MapReduce mood distribution mengagregasi mood
    dengan benar dari data dummy.
    """
    test_dir = tmp_path / "testdb_mapreduce_mood"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("MoodUser")
    spark_analytics.generate_dummy_data(jumlah_journal=40, jumlah_todo=5, jumlah_mood=5)

    report = spark_analytics.get_analytics_report()

    # Mood distribution harus ada
    assert len(report["mood_distribution"]) > 0

    # Total mood harus sama dengan jumlah jurnal
    total_mood_count = sum(count for _, count in report["mood_distribution"])
    assert total_mood_count == report["total_journal_processed"]


def test_empty_database_no_crash(tmp_path, monkeypatch):
    """
    Pastikan analisis MapReduce pada database kosong tidak crash dan
    mengembalikan data kosong yang valid dengan 2 partisi [0, 0].
    """
    test_dir = tmp_path / "testdb_mapreduce_empty"
    test_dir.mkdir()
    monkeypatch.chdir(test_dir)

    database.set_active_user("EmptyUser")

    report = spark_analytics.get_analytics_report()

    assert report["total_journal_processed"] == 0
    assert report["total_todo_processed"] == 0
    assert report["todo_completion_rate"] == 0.0
    assert report["word_frequency"] == []
    assert report["mood_distribution"] == []
    assert report["num_partitions"] == 2


def test_pyspark_available_flag():
    """
    Verifikasi bahwa flag PYSPARK_AVAILABLE diatur berdasarkan
    apakah library pyspark terinstal.
    """
    assert isinstance(spark_analytics.PYSPARK_AVAILABLE, bool)


def test_num_partitions_constant():
    """
    Pastikan konstanta NUM_PARTITIONS minimal 2 sesuai
    persyaratan dosen (minimal 2 node).
    """
    assert spark_analytics.NUM_PARTITIONS >= 2
