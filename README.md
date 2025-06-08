# 🧠 AI-Health Backend (Django + ML)

Ini adalah backend aplikasi berbasis Django yang mengintegrasikan fitur AI/ML untuk mendiagnosis penyakit berdasarkan gejala pengguna. Backend ini juga menyediakan REST API untuk login, registrasi, dan manajemen data seperti pasien, dokter, gejala, diagnosis, dan riwayat diagnosis.

---

## 🚀 Fitur Utama

* 🔐 Autentikasi (login/register) untuk pasien dan dokter
* 📄 Manajemen data:

  * Pasien & Dokter
  * Gejala & Penyakit
  * Jadwal Dokter
  * Riwayat Diagnosis
* 🧠 Prediksi penyakit berdasarkan input gejala (model ML)
* 📡 REST API siap digunakan oleh frontend (mobile/web)

---

## 🧱 Teknologi yang Digunakan

* **Django** - Backend utama
* **Django REST Framework** - Untuk membangun REST API
* **Scikit-learn / TensorFlow / PyTorch** - Untuk inference model AI (sesuaikan)
* **SQLite / PostgreSQL** - Database
* **Python 3.8+**

---

## 📂 Struktur Folder

```
ai_health_backend/
├── diagnose_ai/         # Aplikasi Django untuk fitur diagnosis AI
├── users/               # Aplikasi Django untuk login/register
├── core/                # Konfigurasi utama Django
├── db.sqlite3           # (Contoh) Database SQLite
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalasi dan Menjalankan Server

1. **Clone repository**:

   ```bash
   git clone https://github.com/username/ai-health-backend.git
   cd ai-health-backend
   ```

2. **Buat virtual environment dan aktifkan**:

   ```bash
   python -m venv env
   source env/bin/activate  # atau `env\Scripts\activate` di Windows
   ```

3. **Install dependensi**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan migrasi database**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Jalankan server lokal**:

   ```bash
   python manage.py runserver
   ```

---

## 🧠 Model AI

Model AI telah dilatih menggunakan `scikit-learn` (atau TensorFlow/PyTorch). Model dimuat di backend dan digunakan saat endpoint `/api/diagnose/` dipanggil.

Model file: `model/diagnosis_model.pkl` *(contoh)*

---

## 👩‍💼 Kontributor

* 🧑 Brian Alexander
* 🧑 Kinsley Reynard Tanjung
* 🧑 Kenneth Nathanael Yuwono
* 🧑 Nathaniel Wijaya

---

> 🚧 Masih dalam tahap pengembangan.
