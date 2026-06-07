import psycopg2
from psycopg2.extras import RealDictCursor
import os

class DB:
    def __init__(self, app=None):
        # Membaca URL koneksi URI langsung dari Environment Variable Azure
        # Jika kosong, otomatis pakai fallback string URI dari Supabase-mu
        self.db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:psokelompok#15@db.xrhqenkwpgiyzffdwdtj.supabase.co:5432/postgres")
        self.connection = None

    def connect(self):
        if self.connection is None or self.connection.closed != 0:
            self.connection = psycopg2.connect(self.db_url)
        return self.connection

    def cur(self):
        # RealDictCursor memaksa output PostgreSQL berbentuk Dictionary (seperti DictCursor di PyMySQL)
        # Langkah ini krusial agar kode Controller & View kelompokmu tidak pecah/eror
        return self.connect().cursor(cursor_factory=RealDictCursor)
        
    def query(self, q):
        # Menyesuaikan sedikit syntax placeholder MySQL jika ada (misal mengubah @table menjadi nama tabel asli)
        cursor = self.cur()
        cursor.execute(q)
        # Otomatis melakukan commit jika ada query INSERT/UPDATE/DELETE
        if any(keyword in q.upper() for keyword in ["INSERT", "UPDATE", "DELETE", "ALTER", "DROP"]):
            self.connect().commit()
        return cursor