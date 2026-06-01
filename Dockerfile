# 1. Menggunakan base image resmi Python berbasis Linux alpine agar ukuran kontainer ringan
FROM python:3.11-slim

# 2. Mengatur environment variable agar output Python langsung dicetak ke log tanpa di-buffer
ENV PYTHONUNBUFFERED=1

# 3. Menetapkan folder kerja di dalam kontainer Docker
WORKDIR /app

# 4. Menyalin berkas dependensi pip terlebih dahulu untuk memanfaatkan Docker layer caching
COPY requirements.txt .

# 5. Memasang pustaka pemrograman Flask dan dependensi database relasional
RUN pip install --no-cache-dir -r requirements.txt

# 6. Menyalin seluruh berkas arsitektur aplikasi (App, Controllers, Models, routes, static, templates)
COPY . .

# 7. Membuka port internal dokumen web (Flask default port)
EXPOSE 5000

# 8. Perintah utama untuk menjalankan aplikasi web menggunakan WSGI server (Gunicorn) demi performa production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]