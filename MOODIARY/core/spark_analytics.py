# core/spark_analytics.py
# ==============================================================================
# MOODIARY - APACHE PYSPARK BIG DATA ANALYTICS ENGINE (DUAL-ENGINE ARCHITECTURE)
# ==============================================================================
# Modul ini mengimplementasikan pemrosesan data analitik menggunakan konsep
# MapReduce pada Apache PySpark. Data dummy dibuat untuk mensimulasikan data
# raya (Big Data) yang dipecah ke dalam minimal 2 node/partisi agar dapat
# diproses secara paralel dan terdistribusi.
# ==============================================================================
import re
import random
from datetime import datetime, timedelta
from collections import Counter
import core.database as database

PYSPARK_AVAILABLE = False
try:
    import pyspark
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, explode, split, lower, trim, count as spark_count
    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False

# ==============================================================================
# KONFIGURASI MAPREDUCE
# ==============================================================================
NUM_PARTITIONS = 2  # Jumlah node/partisi minimum sesuai perintah dosen

STOP_WORDS = {
    "yang", "dan", "di", "dari", "ke", "untuk", "pada", "dengan", "adalah",
    "ini", "itu", "saya", "kamu", "dia", "kita", "akan", "telah", "sudah",
    "bisa", "agar", "dalam", "atau", "saat", "hari", "juga", "sangat", "lebih",
    "ada", "oleh", "bagi", "secara", "sebagai", "namun", "tetapi", "karena",
    "tidak", "lagi", "banyak", "semua", "mereka", "kami", "begitu", "harus",
    "serta", "setiap", "masih", "sebuah", "ketika", "sedang", "seperti", "bahwa",
    "maka", "menjadi", "terhadap", "antara", "tentang", "beberapa", "tersebut"
}


# ==============================================================================
# GENERATOR DATA DUMMY
# ==============================================================================
DUMMY_JUDUL = [
    "Hari Pertama Kuliah Semester Baru",
    "Presentasi Tugas Akhir yang Menegangkan",
    "Belajar Framework Python Flask di Lab Komputer",
    "Proyek Kelompok Big Data Analytics Selesai",
    "Seminar Nasional Teknologi Informasi",
    "Kelas Pemrograman Python Lanjut",
    "Ujian Tengah Semester Sistem Basis Data",
    "Workshop Machine Learning dan Kecerdasan Buatan",
    "Latihan Coding Challenge Hackathon Kampus",
    "Diskusi Ilmiah Tentang Cloud Computing",
    "Praktikum Jaringan Komputer di Laboratorium",
    "Mengerjakan Laporan Algoritma dan Struktur Data",
    "Review Paper Jurnal Internasional Data Science",
    "Persiapan Lomba Kompetisi Programming",
    "Tutorial Apache Spark untuk Pengolahan Data",
    "Studi Kasus Implementasi Sistem Informasi",
    "Membuat Aplikasi Mobile dengan React Native",
    "Analisis Sentimen Media Sosial Twitter",
    "Pertemuan Himpunan Mahasiswa Informatika",
    "Mengikuti Webinar Cybersecurity Nasional",
    "Kelas Statistika Probabilitas dan Matematika Diskrit",
    "Tugas Besar Pemrosesan Bahasa Natural",
    "Evaluasi Kinerja Algoritma Sorting",
    "Pengembangan Website Portal Akademik",
    "Bimbingan Skripsi dengan Dosen Pembimbing",
    "Menyelesaikan Modul E-Learning Platform",
    "Kompetisi Desain Interface Pengguna",
    "Membuat Dashboard Visualisasi Data",
    "Pelatihan Git dan Version Control System",
    "Riset Topik Kecerdasan Buatan Generatif",
]

DUMMY_ISI = [
    "Hari ini saya mengikuti kelas pemrograman Python dan belajar tentang framework Django serta bagaimana membangun aplikasi web modern. Dosen memberikan tugas proyek kelompok yang cukup menantang.",
    "Presentasi tugas akhir berjalan dengan lancar. Tim kami berhasil mendemonstrasikan aplikasi analisis data menggunakan teknologi Apache Spark yang mampu memproses dataset berukuran besar secara efisien.",
    "Menghadiri seminar nasional tentang transformasi digital dan penerapan kecerdasan buatan dalam dunia pendidikan. Banyak insight baru tentang machine learning yang didapatkan.",
    "Proyek kelompok sistem informasi akhirnya selesai setelah dua minggu bekerja keras. Aplikasi berhasil diimplementasikan menggunakan arsitektur microservices dan teknologi cloud computing.",
    "Ujian tengah semester mata kuliah basis data cukup sulit. Soal tentang normalisasi database dan optimasi query SQL membutuhkan pemahaman mendalam tentang konsep relasional.",
    "Workshop pengembangan aplikasi mobile memberikan pengalaman praktis tentang React Native dan Flutter. Peserta diajarkan cara membangun aplikasi cross-platform yang responsif.",
    "Latihan coding untuk persiapan kompetisi hackathon kampus sangat intensif. Fokus pada algoritma sorting, searching, dan pemrograman dinamis menggunakan bahasa Python.",
    "Diskusi kelompok tentang implementasi blockchain dalam sistem keamanan data. Topik yang sangat menarik tentang teknologi desentralisasi dan smart contract.",
    "Praktikum jaringan komputer hari ini membahas konfigurasi router, switch, dan firewall. Simulasi menggunakan Cisco Packet Tracer sangat membantu pemahaman konsep networking.",
    "Mengerjakan laporan penelitian tentang perbandingan algoritma machine learning untuk klasifikasi sentimen pada review produk e-commerce menggunakan dataset yang sangat besar.",
    "Belajar tentang konsep MapReduce pada Apache Hadoop dan PySpark untuk pemrosesan data raya. Memahami bagaimana data dipecah ke beberapa node untuk pemrosesan paralel.",
    "Kelas statistika membahas distribusi probabilitas, regresi linier, dan analisis variansi. Konsep ini sangat penting untuk pemahaman data science dan analytics.",
    "Membuat visualisasi dashboard interaktif menggunakan library Matplotlib, Seaborn, dan Plotly untuk menampilkan tren data penjualan perusahaan selama satu tahun terakhir.",
    "Pelatihan intensif Git version control system untuk kolaborasi pengembangan software secara tim. Mempelajari branching, merging, dan resolusi konflik dalam repositori kode.",
    "Riset mandiri tentang arsitektur transformer dan model bahasa besar seperti GPT dan BERT untuk tugas natural language processing dan pemrosesan bahasa natural.",
    "Evaluasi performa berbagai algoritma sorting seperti QuickSort, MergeSort, dan HeapSort dengan kompleksitas waktu dan ruang yang berbeda pada dataset berukuran bervariasi.",
    "Mengikuti webinar tentang keamanan siber dan ethical hacking. Memahami teknik penetration testing dan vulnerability assessment untuk mengamankan sistem informasi.",
    "Mengembangkan REST API menggunakan FastAPI Python untuk backend sistem manajemen perpustakaan digital. Implementasi autentikasi JWT dan validasi data menggunakan Pydantic.",
    "Bimbingan skripsi membahas metodologi penelitian kuantitatif dan teknik pengumpulan data untuk studi perbandingan framework pengembangan aplikasi web modern.",
    "Menyelesaikan modul pembelajaran online tentang Amazon Web Services dan Google Cloud Platform. Mendapatkan sertifikasi dasar cloud computing.",
    "Tugas besar mata kuliah pemrosesan bahasa natural mengharuskan implementasi tokenisasi, stemming, dan analisis sentimen menggunakan library NLTK dan SpaCy Python.",
    "Kompetisi desain antarmuka pengguna tingkat fakultas menampilkan kreativitas mahasiswa dalam merancang user experience yang intuitif dan aksesibel.",
    "Mengerjakan proyek akhir mata kuliah data warehouse dan business intelligence. Membangun ETL pipeline untuk mengintegrasikan data dari berbagai sumber database.",
    "Kelas kecerdasan buatan membahas neural network, deep learning, dan convolutional neural network untuk pengenalan gambar dan klasifikasi objek visual.",
    "Berpartisipasi dalam program magang virtual di startup teknologi. Mengerjakan fitur pencarian cerdas menggunakan Elasticsearch dan algoritma rekomendasi berbasis kolaboratif.",
]

DUMMY_MOODS = ["Gembira", "Semangat", "Biasa Saja", "Sedih", "Cemas", "Marah", "Bersyukur", "Bahagia"]
DUMMY_KATEGORI = ["Kuliah", "Teknologi", "Pribadi", "Proyek", "Karir", "Organisasi"]
DUMMY_TUGAS = [
    ("Selesaikan laporan PySpark", "Menulis laporan praktikum Apache Spark", "Tinggi"),
    ("Review jurnal ilmiah", "Membaca dan merangkum 3 paper internasional", "Tinggi"),
    ("Submit tugas algoritma", "Upload kode sorting ke e-learning", "Tinggi"),
    ("Latihan soal UTS", "Kerjakan bank soal basis data", "Tinggi"),
    ("Buat presentasi seminar", "Slide tentang big data analytics", "Sedang"),
    ("Konfigurasi server lab", "Setup Apache Hadoop cluster lokal", "Sedang"),
    ("Meeting kelompok proyek", "Diskusi pembagian tugas akhir", "Sedang"),
    ("Coding challenge harian", "Selesaikan problem HackerRank", "Sedang"),
    ("Baca dokumentasi Spark", "Pelajari RDD dan DataFrame API", "Rendah"),
    ("Update portofolio GitHub", "Push project terbaru ke repo", "Rendah"),
    ("Install library Python", "Setup environment PySpark", "Rendah"),
    ("Backup database lokal", "Export data SQLite ke JSON", "Rendah"),
]


def generate_dummy_data(jumlah_journal=50, jumlah_todo=20, jumlah_mood=30):
    """
    Membuat data dummy yang realistis dan menyimpannya ke dalam database
    SQLite pengguna aktif. Data ini mensimulasikan dataset besar (Big Data)
    yang akan diproses oleh engine MapReduce PySpark.

    Args:
        jumlah_journal: Jumlah catatan jurnal dummy yang dibuat.
        jumlah_todo: Jumlah tugas to-do dummy yang dibuat.
        jumlah_mood: Jumlah entri mood tracker dummy yang dibuat.

    Returns:
        Dictionary berisi jumlah data yang berhasil dibuat.
    """
    conn = database.get_db_connection()
    cursor = conn.cursor()

    base_date = datetime(2026, 1, 1)

    # 1. Generate Jurnal Dummy
    for i in range(jumlah_journal):
        tanggal = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        judul = random.choice(DUMMY_JUDUL)
        isi = random.choice(DUMMY_ISI)
        mood = random.choice(DUMMY_MOODS)
        kategori = random.choice(DUMMY_KATEGORI)
        cursor.execute(
            "INSERT INTO journal (tanggal, judul, isi, mood, kategori) VALUES (?, ?, ?, ?, ?)",
            (tanggal, judul, isi, mood, kategori)
        )

    # 2. Generate To-Do Dummy
    for i in range(jumlah_todo):
        tugas, detail, prioritas = random.choice(DUMMY_TUGAS)
        deadline = (base_date + timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        selesai = random.choice([0, 0, 0, 1, 1])  # 40% selesai
        cursor.execute(
            "INSERT INTO todo (tugas, detail, prioritas, deadline, selesai) VALUES (?, ?, ?, ?, ?)",
            (tugas, detail, prioritas, deadline, selesai)
        )

    # 3. Generate Mood Tracker Dummy
    for i in range(jumlah_mood):
        tanggal = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        mood = random.choice(DUMMY_MOODS)
        catatan = f"Mood hari ke-{i+1}: {mood}"
        cursor.execute(
            "INSERT INTO mood (tanggal, mood, catatan) VALUES (?, ?, ?)",
            (tanggal, mood, catatan)
        )

    conn.commit()
    conn.close()

    return {
        "journal_created": jumlah_journal,
        "todo_created": jumlah_todo,
        "mood_created": jumlah_mood,
        "total_records": jumlah_journal + jumlah_todo + jumlah_mood
    }

