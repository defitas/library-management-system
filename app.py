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
        
        # 1. Cek apakah tabel 'user' atau 'users' sudah ada
        cursor.execute("SHOW TABLES LIKE 'user';")
        user_table_exists = cursor.fetchone()
        
        # 2. Jika tabel belum terbentuk sama sekali, coba jalankan file lms.sql
        if not user_table_exists:
            print("Database Azure kosong. Menjalankan pembentukan skema...")
            with open('db/lms.sql', 'r', encoding='utf-8') as f:
                sql_file = f.read()
                # Membagi query berdasarkan semicolon, mengabaikan baris kosong
                sql_commands = [cmd.strip() for cmd in sql_file.split(';') if cmd.strip()]
                
                for command in sql_commands:
                    try:
                        cursor.execute(command)
                    except Exception as sql_err:
                        print(f"Log info pembuatan: {sql_err}")
            db.commit()

        # 3. Paksa kolom id menjadi AUTO_INCREMENT secara manual
        print("Menjalankan paksa perbaikan AUTO_INCREMENT di Azure Flexible Server...")
        
        # Perbaikan untuk tabel admin
        try:
            cursor.execute("ALTER TABLE admin MODIFY COLUMN id INT AUTO_INCREMENT;")
            db.commit()
            print("AUTO_INCREMENT pada tabel admin sukses diterapkan!")
        except Exception as e_admin:
            print(f"Catatan tabel admin: {e_admin}")
            
        # Perbaikan untuk tabel users
        try:
            cursor.execute("ALTER TABLE users MODIFY COLUMN id INT AUTO_INCREMENT;")
            db.commit()
            print("AUTO_INCREMENT pada tabel users sukses diterapkan!")
        except Exception as e_users:
            print(f"Catatan tabel users: {e_users}")

except Exception as e:
    print(f"Gagal total mengeksekusi inisialisasi awal database: {e}")

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