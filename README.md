# 🎵 MusicPython

**MusicPython** adalah proyek berbasis Python yang dirancang untuk memutar dan menampilkan lagu *Soulsoup* karya **Official HIGE DANdism**.

Proyek ini mendemonstrasikan penggunaan Python untuk mengintegrasikan berbagai aset multimedia, seperti audio, gambar sampul, lirik, dan font kustom, guna menciptakan pengalaman pemutaran musik yang sederhana.

## ✨ Fitur

- 🎧 **Pemutaran Audio** — Memutar lagu *Soulsoup* melalui aplikasi Python.
- 🖼️ **Tampilan Sampul Lagu** — Menampilkan gambar sampul dari folder `covers/`.
- 📝 **Tampilan Lirik** — Menyediakan aset lirik yang tersimpan di folder `lyrics/`.
- 🔤 **Font Kustom** — Mendukung penggunaan font tambahan dari folder `fonts/`.
- 📁 **Manajemen Aset** — Mengorganisasi file audio dan aset visual dalam struktur direktori yang terpisah.

## 📂 Struktur Direktori

Berikut adalah struktur direktori proyek MusicPython:

```text
MusicPython/
├── covers/       # Gambar sampul lagu
├── fonts/        # Font kustom untuk tampilan teks
├── lyrics/       # File lirik lagu
├── music/        # File audio (.mp3/.wav)
└── soulsoup.py   # Script utama aplikasi
```

## 🚀 Cara Menjalankan

### 1. Persyaratan

Pastikan perangkatmu sudah memiliki:

- Python yang telah terinstal.
- Git untuk mengunduh repositori.
- Library tambahan yang dibutuhkan oleh aplikasi.

> **Catatan:** Library yang diperlukan bergantung pada implementasi di dalam `soulsoup.py`. Jika proyek menggunakan Pygame, ikuti langkah instalasi berikut.

### 2. Instalasi Library

Jika aplikasi menggunakan Pygame, jalankan perintah berikut di terminal:

```bash
pip install pygame
```

### 3. Unduh Repositori

Kloning repositori dari GitHub:

```bash
git clone https://github.com/qanziz47-coder/MusicPython.git
```

Masuk ke direktori proyek:

```bash
cd MusicPython
```

### 4. Jalankan Aplikasi

Jalankan script utama dengan perintah:

```bash
python soulsoup.py
```

Pastikan file audio dan aset pendukung tersedia di direktori yang sesuai sebelum menjalankan aplikasi.

## 🛠️ Teknologi yang Digunakan

- **Python** — Bahasa pemrograman utama.
- **Pygame** — Kandidat library untuk pemutaran audio, jika digunakan dalam kode.
- **Aset Multimedia** — File audio, gambar, lirik, dan font pendukung.

*Catatan: Teknologi dan library yang tercantum perlu disesuaikan dengan implementasi sebenarnya di dalam kode proyek.*

## 👤 Author

**Fajri Hafz**

GitHub: [@qanziz47-coder](https://github.com/qanziz47-coder)

## 📄 Lisensi

Lisensi proyek belum dicantumkan. Silakan tambahkan informasi lisensi jika proyek ini akan dibagikan atau dikembangkan secara terbuka.

---

Dibuat dengan ❤️ menggunakan Python.
