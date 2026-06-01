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
        cursor.execute("SHOW TABLES LIKE 'admin';")
        result = cursor.fetchone()
        
        if not result:
            print("Database kosong. Memulai pembentukan skema otomatis...")
            with open('db/lms.sql', 'r') as f:
                # Menggunakan gunicorn/linux splitter yang aman
                sql_commands = f.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
            db.commit()
            print("Skema database lms.sql berhasil terbentuk!")
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