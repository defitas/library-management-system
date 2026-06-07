import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DB:
    def __init__(self, app=None):
        # Membaca URL koneksi URI langsung dari Environment Variable Azure
        # Jika kosong, otomatis pakai fallback string URI dari Supabase kelompok 15
        self.db_url = os.environ.get("DATABASE_URL")
        self.connection = None

    def connect(self):
        if self.connection is None or self.connection.closed != 0:
            # Mengaktifkan autocommit opsional agar koneksi tidak menggantung di Supabase
            self.connection = psycopg2.connect(self.db_url)
        return self.connection

    def cur(self):
        # RealDictCursor memaksa output PostgreSQL berbentuk Dictionary
        return self.connect().cursor(cursor_factory=RealDictCursor)
        
    def query(self, q, params=None):
        cursor = self.cur()
        try:
            cursor.execute(q, params)  # params handles safe substitution
            if any(keyword in q.upper() for keyword in ["INSERT", "UPDATE", "DELETE", "ALTER", "DROP"]):
                  self.connect().commit()
            return cursor
        except Exception as e:
            # Jika gagal, batalkan transaksi agar database tidak terkunci (Lock)
            if self.connection:
                self.connection.rollback()
            raise e