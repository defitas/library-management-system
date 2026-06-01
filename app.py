from flask import Flask, g, escape, session, redirect, render_template, request, jsonify, Response
from Misc.functions import *
from Models.DAO import DAO 

app = Flask(__name__)
app.secret_key = '#$ab9&^BB00_.'

# 1. Inisialisasi DAO terlebih dahulu agar objek database (__init__ di DB.py) terbentuk
DAO = DAO(app)
db = DAO.db # Ambil objek koneksi database dari DAO kelompokmu

# 2. Jalankan skrip inisialisasi otomatis skema lms.sql
try:
    with app.app_context():
        cursor = db.cur()
        
        print("Menjalankan skrip perbaikan AUTO_INCREMENT di Azure...")
        try:
            cursor.execute("ALTER TABLE admin MODIFY COLUMN id INT AUTO_INCREMENT;")
            db.commit()
            print("Tabel admin berhasil diperbaiki!")
        except Exception as e_admin:
            print(f"Tabel admin mungkin sudah auto_increment: {e_admin}")

        try:
            cursor.execute("ALTER TABLE user MODIFY COLUMN id INT AUTO_INCREMENT;")
            db.commit()
            print("Tabel user berhasil diperbaiki!")
        except Exception as e_user:
            print(f"Tabel user mungkin sudah auto_increment: {e_user}")

except Exception as e:
    print(f"Gagal total eksekusi perintah: {e}")

# Registering blueprints
from routes.user import user_view
from routes.book import book_view
from routes.admin import admin_view

# Registering custom functions to be used within templates
app.jinja_env.globals.update(
    ago=ago,
    str=str,
)

app.register_blueprint(user_view)
app.register_blueprint(book_view)
app.register_blueprint(admin_view)