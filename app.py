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
        
        # Cek apakah tabel utama 'users' sudah ada
        cursor.execute("SHOW TABLES LIKE 'users';")
        tables_exist = cursor.fetchone()
        
        if not tables_exist:
            print("Database kosong atau belum optimal. Memulai migrasi lms.sql bersih...")
            with open('db/lms.sql', 'r', encoding='utf-8') as f:
                sql_file = f.read()
                sql_commands = [cmd.strip() for cmd in sql_file.split(';') if cmd.strip()]
                
                for command in sql_commands:
                    try:
                        cursor.execute(command)
                    except Exception as run_err:
                        print(f"Info eksekusi query: {run_err}")
            db.commit()
            print("Seluruh skema database baru berhasil terpasang sempurna!")
            
except Exception as e:
    print(f"Gagal menginisialisasi database: {e}")

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