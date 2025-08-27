# SIAKAD - Sistem Informasi Akademik Sekolah

Sebuah aplikasi web untuk mengelola sistem informasi akademik sekolah yang dikembangkan menggunakan Flask dan Bootstrap.

## Fitur Utama

- 🔐 **Sistem Autentikasi** - Login dan logout yang aman
- 👨‍🎓 **Manajemen Siswa** - Tambah, lihat, edit, dan hapus data siswa
- 👨‍🏫 **Manajemen Guru** - Kelola data guru dan mata pelajaran
- 🏫 **Manajemen Kelas** - Atur kelas dan wali kelas
- 📊 **Dashboard Informatif** - Statistik dan grafik data sekolah
- 📱 **Responsive Design** - Tampilan yang menyesuaikan berbagai perangkat
- 🎨 **Modern UI/UX** - Interface yang user-friendly dan menarik

## Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Database**: SQLite (dapat diganti dengan PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5
- **Icons**: Font Awesome
- **Charts**: Chart.js

## Struktur Project

```
siakad/
├── app.py                 # Aplikasi utama Flask
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi project
├── siakad.db             # Database SQLite (akan dibuat otomatis)
├── templates/            # Template HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── teachers.html
│   ├── add_teacher.html
│   └── classes.html
└── static/              # File statis
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

## Instalasi

### 1. Clone atau Download Project

```bash
git clone <repository-url>
cd siakad
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
python app.py
```

### 4. Akses Aplikasi

Buka browser dan akses: `http://localhost:5000`

## Login Default

- **Username**: `admin`
- **Password**: `admin123`

## Penggunaan

### Dashboard
- Menampilkan statistik jumlah siswa, guru, kelas, dan mata pelajaran
- Grafik distribusi siswa per kelas
- Timeline aktivitas terbaru
- Quick actions untuk operasi cepat

### Manajemen Siswa
- **Tambah Siswa**: Formulir lengkap dengan validasi
- **Lihat Data**: Tabel dengan fitur pencarian dan filter
- **Detail Siswa**: Modal popup dengan informasi lengkap
- **Export Data**: CSV dan print (coming soon)

### Manajemen Guru
- **Tambah Guru**: Form dengan mata pelajaran dan kualifikasi
- **Daftar Guru**: Tabel terorganisir dengan filter
- **Info Detail**: Profil guru dan kelas yang diajar

### Manajemen Kelas
- **Buat Kelas**: Setup kelas baru dengan wali kelas
- **Overview Kelas**: Card view dengan statistik
- **Detail Kelas**: Daftar siswa dan informasi lengkap

## Konfigurasi Database

### SQLite (Default)
Database SQLite akan dibuat otomatis di `siakad.db`

### PostgreSQL (Production)
Ubah konfigurasi di `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/siakad'
```

### MySQL
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/siakad'
```

## Deployment

### 1. Production Setup

```bash
# Install gunicorn
pip install gunicorn

# Run dengan gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### 2. Environment Variables

```bash
export SECRET_KEY=your-secret-key-here
export DATABASE_URL=your-database-url
export FLASK_ENV=production
```

### 3. Nginx Configuration (Optional)

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Kontribusi

1. Fork repository ini
2. Buat branch feature baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Roadmap Pengembangan

- [ ] Sistem penilaian dan rapor
- [ ] Manajemen jadwal pelajaran
- [ ] Absensi digital
- [ ] Komunikasi orang tua-sekolah
- [ ] Laporan dan analytics
- [ ] Mobile app
- [ ] API untuk integrasi
- [ ] Multi-sekolah support

## Troubleshooting

### Database Error
```bash
# Reset database
rm siakad.db
python app.py
```

### Port sudah digunakan
```bash
# Cek process yang menggunakan port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Permission Error
```bash
# Pastikan memiliki permission untuk write
chmod 755 .
```

## Support

Jika mengalami masalah atau memiliki pertanyaan:

1. Cek bagian Troubleshooting di atas
2. Buat issue di GitHub repository
3. Hubungi developer

## License

Project ini menggunakan MIT License. Silakan lihat file `LICENSE` untuk detail lebih lanjut.

## Acknowledgments

- Bootstrap untuk framework CSS
- Font Awesome untuk icons
- Chart.js untuk visualisasi data
- Flask community untuk dokumentasi yang excellent

---

**Dibuat dengan ❤️ untuk kemajuan pendidikan Indonesia**