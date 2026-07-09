# 🌸 Moodiary v2 — Aplikasi Manajemen Kesejahteraan Mental & Big Data Analytics


![Moodiary Banner](https://img.shields.io/badge/Moodiary-v2.0%20Enterprise%20Edition-F06292?style=for-the-badge&logo=heart&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-FFE082?style=for-the-badge&logo=python&logoColor=black)
![Apache PySpark](https://img.shields.io/badge/Apache%20PySpark-MapReduce%20Big%20Data-E65100?style=for-the-badge&logo=apachespark&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Multi--User%20Isolation-4FC3F7?style=for-the-badge&logo=sqlite&logoColor=black)


**Moodiary v2** adalah aplikasi desktop modern berbasis Python Tkinter yang dirancang khusus untuk memadukan **Kesehatan Mental (Mental Wellness)**, **Produktivitas Pribadi**, dan **Pemrosesan Data Raya (Big Data Analytics) menggunakan Apache PySpark MapReduce**.


Aplikasi ini dikembangkan sebagai tugas akhir mata kuliah **Data Raya dan Pemrograman** pada **Program Studi Psikologi**.


---


## 👥 Kredit Tim Pengembang


Proyek ini disusun dan dikembangkan oleh tim mahasiswa **Program Studi Psikologi**:


| Peran | Nama Lengkap | NIM |
| :--- | :--- | :--- |
| **Ketua** | **Lailli Nur Fajri** | `1801624036` |
| **Anggota Pertama** | **Najla Ratnamaya Syafnita** | `1801624182` |
| **Anggota Kedua** | **Donna Oktaviani Shabila** | `1801624003` |


* **Mata Kuliah:** Data Raya dan Pemrograman  
* **Program Studi:** Psikologi  


---


## 🏗️ Arsitektur Sistem & Desain Perangkat Lunak


Moodiary v2 dirancang dengan prinsip **Modular Architecture**, **Single-Window Frame Controller**, serta **Multi-User Database Isolation** untuk memastikan keamanan privasi, kemudahan navigasi, dan skalabilitas data.


```
Moodiary v2/
├── main.py                   # Entry point & Single-Window Frame Controller
├── core/                     # Lapisan Inti (Core Engine & Logika Bisnis)
│   ├── database.py           # Multi-User SQLite Database Manager & JSON Portability
│   ├── spark_analytics.py    # Apache PySpark MapReduce Engine (2 Node / Dual-Engine)
│   ├── i18n.py               # Internationalization & Language Management (ID / EN)
│   └── theme.py              # Design Tokens, Palet Warna, & Konsistensi UI GUI
├── views/                    # Lapisan Presentasi (Antarmuka Pengguna / GUI Tkinter)
│   ├── login_view.py         # Otentikasi Pengguna Masuk
│   ├── register_view.py      # Pendaftaran Akun Baru
│   ├── daily_journal_view.py # Catatan Jurnal Harian (CRUD)
│   ├── mood_tracker_view.py  # Pelacakan Suasana Hati & Emosi
│   ├── todo_list_view.py     # Manajemen Tugas & Produktivitas
│   ├── wish_list_view.py     # Daftar Impian & Target Masa Depan
│   ├── analytics_view.py     # Executive Analytics Dashboard (4 Tab + PySpark MapReduce)
│   ├── settings_view.py      # Pengaturan Bahasa, Akun, Keamanan, & Export/Import JSON
│   └── quotes_view.py        # Kutipan Inspiratif Harian Dwibahasa
└── tests/                    # Automated Integration & Unit Test Suite (Pytest)
    ├── test_single_window.py # Pengujian UI Frame & Navigasi
    ├── test_ui_integrity.py  # Pengujian Isolasi DB, Tema, & Portabilitas JSON
    └── test_pyspark_analytics.py # Pengujian MapReduce & Big Data Pipeline
```


---


## 🔬 Sorotan Arsitektur Utama


### 1. 🛡️ Multi-User Database Isolation (`core/database.py`)
* **Isolasi Penuh Antar Akun:** Setiap pengguna memiliki database privat tersendiri bernama `moodiary_<username>.db`. Hal ini menjamin bahwa catatan pribadi, suasana hati, dan impian seorang pengguna tidak dapat diakses atau bercampur dengan akun lain.
* **Otentikasi Terpusat:** Kredensial login dikelola secara terpisah dalam file pusat `users.db`.
* **Pemeliharaan Identitas Dinamis (`rename_user_db`):** Saat pengguna mengubah nama akun/username di Pengaturan, sistem secara otomatis merename file database lama (`moodiary_lama.db` ➔ `moodiary_baru.db`) sehingga seluruh catatan historis dipertahankan secara utuh 100%.
* **Portabilitas Data JSON:** Mendukung penuh fitur **Export Data ke JSON** dan **Import Data dari JSON** untuk keperluan pencadangan (*backup*) dan pemulihan (*restore*) seluruh modul.


---


### 2. ⚡ Apache PySpark MapReduce Big Data Engine (`core/spark_analytics.py`)
Sesuai dengan kurikulum **Data Raya dan Pemrograman**, Moodiary v2 dilengkapi dengan mesin pemrosesan data berskala besar menggunakan paradigma **MapReduce** pada **Apache PySpark**:
* **Simulasi Big Data (Dummy Data Generator):** Tombol **Generate Data Dummy** menghasilkan 100+ record terstruktur (50 jurnal, 20 tugas produktivitas, dan 30 entri mood) untuk mensimulasikan pemrosesan data raya.
* **Partisi Data 2 Node (`repartition(2)`):** Dataset dipecah ke dalam **minimal 2 partisi/node eksekusi paralel** untuk mensimulasikan komputasi terdistribusi yang sesungguhnya.
* **Alur Kerja MapReduce PySpark:**
  1. **Partitioning:** Membagikan dataset ke 2 node eksekutor (`parallelize(..., 2)`).
  2. **Map Phase:** Setiap dokumen jurnal dipecah menjadi token kata berskala besar dan ditransformasikan menjadi pasangan key-value `(kata, 1)`. Filter otomatis menghilangkan *stop words* bahasa Indonesia.
  3. **Reduce Phase:** Melakukan komputasi agregasi terdistribusi (`reduceByKey(lambda a, b: a + b)`) untuk menemukan **Top 10 Kata Kunci Dominan** dan **Distribusi Suasana Hati Pengguna**.
* **Dual-Engine Graceful Fallback:** Sistem secara cerdas mendeteksi ketersediaan library `pyspark`. Jika Java/Hadoop belum dikonfigurasi di komputer pengguna, aplikasi otomatis beralih ke *Built-in Python Fallback MapReduce Engine* yang mereplikasi partisi 2 node dan keluaran identik tanpa pernah mengalami *crash*.


---


### 3. 🖥️ Single-Window Frame Rendering Architecture (`main.py`)
* Menghilangkan pembukaan jendela pop-up (`Toplevel`) yang bertumpuk. Seluruh perpindahan menu, dasbor, form input, hingga statistik dieksekusi melalui pertukaran frame dalam satu jendela utama yang bersih dan profesional.


---


### 4. 🌐 Sistem Dwibahasa Real-Time (`core/i18n.py`)
* Seluruh antarmuka, kutipan motivasi harian (*Daily Quotes*), label tombol, dan notifikasi mendukung peralihan instan antara **Bahasa Indonesia (`ID`)** dan **English (`EN`)**.


---


## 📊 Fitur Utama Aplikasi


1. **📖 Catatan Jurnal Harian (Daily Journal):** Tulis refleksi diri, simpan pengalaman harian, serta kelompokkan berdasarkan kategori emosi dan topik kehidupan.
2. **😊 Pelacak Suasana Hati (Mood Tracker):** Rekam grafik perasaan harian disertai catatan singkat mengenai pemicu emosi.
3. **✅ Manajemen Tugas (To-Do List):** Kelola produktivitas dengan tenggat waktu (*deadline*) dan tingkat prioritas tugas.
4. **🌟 Daftar Impian (Wish List):** Rencanakan target masa depan beserta estimasi biaya dan waktu pencapaian.
5. **📈 Executive Analytics Dashboard:**
   - **Tab 1:** Tren & Grafik Suasana Hati (*Bar Chart Distribusi Emosi*)
   - **Tab 2:** Analisis Produktivitas Tugas (*Progress Bar & Rasio Prioritas*)
   - **Tab 3:** Pencapaian Impian & Kategori Wish List
   - **Tab 4:** **⚡ Apache PySpark MapReduce (2 Node Big Data Analytics)** — Analisis frekuensi kata kunci otomatis dan laporan partisi node.
6. **⚙️ Pengaturan & Preferensi:**
   - Pengaturan Bahasa Aplikasi (ID/EN)
   - Manajemen Keamanan Akun (Ganti Username & Password)
   - Portabilitas Basis Data (Export & Import file `.json`)


---


## 🚀 Panduan Instalasi & Menjalankan Aplikasi


### Persyaratan Sistem
* Python 3.10 atau versi lebih baru
* Sistem Operasi: Windows / macOS / Linux


### 1. Instalasi Library Pendukung
Buka terminal/command prompt di dalam folder proyek, lalu instal dependensi yang diperlukan:
```bash
pip install pytest pyspark
```
*(Catatan: Jika `pyspark` tidak diinstal, aplikasi tetap berjalan normal menggunakan mode fallback simulasi MapReduce).*


### 2. Menjalankan Aplikasi
Jalankan file utama melalui terminal:
```bash
python main.py
```


### 3. Menjalankan Automated Test Suite (100% Pass Rate)
Proyek ini dilengkapi dengan 12 unit & integrasi tes otomatis menggunakan `pytest`:
```bash
pytest -v
```


---


## 🎯 Panduan Simulasi Big Data MapReduce untuk Evaluasi Dosen


1. Buka aplikasi dan **Login** atau **Daftar Akun Baru**.
2. Masuk ke menu **📊 Statistik & Analisis** di menu utama dasbor.
3. Klik tab ke-4: **`⚡ PySpark MapReduce (2 Node)`**.
4. Tekan tombol **`📦 Generate Data Dummy (Big Data Simulation)`** dan klik **Yes** pada konfirmasi. Sistem akan membuat **100 record data terstruktur**.
5. Tekan tombol **`🚀 Jalankan MapReduce PySpark (2 Node)`**.
6. Perhatikan keluaran pada layar:
   * **Panel Kiri:** Grafik Horizontal Bar Chart **Top 10 Kata Kunci Jurnal** hasil pemetaan MapReduce.
   * **Panel Kanan:** Laporan lengkap **Konfigurasi Partisi 2 Node** (`Node 1 / Partisi 0` dan `Node 2 / Partisi 1`), jumlah record per partisi, serta hasil reduksi distribusi suasana hati.


---
