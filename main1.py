import polars as pl
import fastexcel
import os

# Path sesuai lokasi di gambar sidebar Colab kamu
file_path = "sample_data/daftar-pemenang-penyedia-tender-pada-kategori-pekerjaan-konstruksi.xlsx"

if not os.path.exists(file_path):
    print("❌ File tidak ditemukan! Pastikan file ada di folder sample_data.")
else:
    try:
        # 1. Baca Workbook secara eksplisit menggunakan fastexcel
        excel = fastexcel.read_excel(file_path)
        
        # 2. Ambil sheet pertama
        sheet_name = excel.sheet_names[0]
        
        # 3. Muat data ke Polars (Coba header_row=2 jika data mulai di baris ke-3)
        df = excel.load_sheet(sheet_name, header_row=2).to_polars()
        
        print("✅ Data Berhasil Terbaca!")
        print(f"Dataset berisi {df.height} baris dan {df.width} kolom.")
        
        # 4. Simpan ke Parquet untuk kebutuhan Training AI MATA RAKYAT
        # Sesuai rencana proposal untuk efisiensi penyimpanan
        df.write_parquet("lkpp_train.parquet")
        df.write_parquet("lkpp_val.parquet")
        
        print("\n💾 SUCCESS! File 'lkpp_train.parquet' sudah siap di folder /content/.")
        print(df.head())

    except Exception as e:
        print(f"❌ Masih ada kendala teknis: {e}")