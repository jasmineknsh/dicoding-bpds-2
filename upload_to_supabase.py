import pandas as pd
from sqlalchemy import create_engine

# === Supabase PostgreSQL URL ===
URL = "postgresql://postgres:jayastudentdrop2@db.asqybnlkwgosvmwwxwpl.supabase.co:5432/postgres"
engine = create_engine(URL)

# === Daftar file dan nama tabel ===
files_and_tables = {
    "data/data.csv": "student",
    "data/eda.csv": "edaData",
    "data/hasil_prediksi2.csv": "hasil_prediksi_mahasiswa",
    "data/10_fitur_paling_penting.csv": "importance_feature"
}

# === Proses upload tiap file ke tabel ===
for file_path, table_name in files_and_tables.items():
    df = pd.read_csv(file_path, encoding='windows-1252')
    df.to_sql(table_name, engine, index=False, if_exists='replace')
    print(f"✅ Berhasil upload ke tabel '{table_name}'")

print("🚀 Semua file berhasil diunggah ke Supabase!")
