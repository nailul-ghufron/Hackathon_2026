import polars as pl
import fastexcel
import os

# Daftar file yang baru kamu upload di sample_data
files_to_process = [
    "sample_data/data-sirup.xlsx",
    "sample_data/data-umkm-yang-mengikuti-pengadaan-barang-dan-jasa-.xlsx"
]

for file_path in files_to_process:
    if not os.path.exists(file_path):
        print(f"❌ File tidak ditemukan: {file_path}")
        continue
        
    try:
        # Baca workbook
        excel = fastexcel.read_excel(file_path)
        sheet_name = excel.sheet_names[0]
        
        # Load ke Polars (Coba header_row=1 atau 2 tergantung format LKPP)
        df = excel.load_sheet(sheet_name, header_row=2).to_polars()
        
        # Buat nama file output Parquet secara otomatis
        output_name = file_path.split('/')[-1].replace('.xlsx', '.parquet')
        df.write_parquet(output_name)
        
        print(f"✅ Berhasil memproses: {file_path} -> {output_name}")
        print(f"   Jumlah baris: {df.height}")
        
    except Exception as e:
        print(f"❌ Gagal memproses {file_path}: {e}")

print("\n💾 Semua file tambahan siap di folder /content/ untuk tahap analisis selanjutnya!")