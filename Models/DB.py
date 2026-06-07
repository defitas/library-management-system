import pymysql
import os

class DB:
    def __init__(self, app=None):
        # 1. Ambil URL koneksi gabungan dari Environment Variable Azure
        # Jika kosong, otomatis pakai fallback string URL publik dari dasbor Railway-mu
        mysql_url = os.environ.get("MYSQL_URL", "mysql://root:nmLYguKztbZBiXtoeLImLsPmZocqZphb@interchange.proxy.rlwy.net:44559/railway")
        
        # 2. Trik cerdas Python untuk memecah string URL menjadi parameter pymysql otomatis
        # Menghapus teks 'mysql://' di depan
        clean_url = mysql_url.replace("mysql://", "")
        
        # Memisahkan bagian user:password dengan bagian host:port/db
        credentials, connection_info = clean_url.split("@")
        user, password = credentials.split(":")
        
        host_port, db_name = connection_info.split("/")
        host, port = host_port.split(":")

        # 3. Masukkan hasil pecahan ke dalam konfigurasi koneksi murni
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None

    def connect(self):
        if self.connection is None or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db_name,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
        return self.connection

    def cur(self):
        return self.connect().cursor()
        
    def query(self, q):
        cursor = self.cur()
        cursor.execute(q)
        return cursor