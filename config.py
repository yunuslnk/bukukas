import pyodbc

# Koneksi ke SQL Server
server = 'localhost'  # Sesuaikan dengan server yang digunakan
database = 'bukukas'  # Nama database
username = 'sa'  # Username SQL Server
password = 'P@ssw0rd'  # Password SQL Server
driver = '{ODBC Driver 17 for SQL Server}'  # Pastikan ODBC driver sesuai

def get_db_connection():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return conn
