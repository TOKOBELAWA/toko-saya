import streamlit as st
import pandas as pd

# 1. Judul Aplikasi
st.set_page_config(page_title="Katalog Harga Toko", page_icon="🛍️")
st.title("🛍️ Cek Harga Produk")
st.write("Cari produk berdasarkan nama atau merk (Contoh: Sunsilk)")

# 2. Fungsi Ambil Data dari Google Sheets
# TTL 60 artinya data akan update otomatis tiap 60 detik jika Excel diubah
@st.cache_data(ttl=60)
def muat_data():
    # LINK DI BAWAH: Ganti dengan link 'Publish to Web' (Format XLSX) dari Google Sheets kamu
    url_sheets = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"
    try:
        df = pd.read_excel(url_sheets)
        # Bersihkan data (hapus spasi di awal/akhir nama)
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = muat_data()

if df is not None:
    # 3. Fitur Pencarian (Sangat Berguna untuk Pelanggan)
    query = st.text_input("🔍 Masukkan Nama Produk:", placeholder="Ketik di sini...")

    if query:
        # Mencari produk yang mengandung kata yang diketik (misal: 'sun' untuk Sunsilk)
        hasil = df[df['Nama_Produk'].str.contains(query, case=False, na=False)]
        
        if not hasil.empty:
            st.success(f"Ditemukan {len(hasil)} produk")
            # Menampilkan hasil dalam bentuk kartu yang rapi
            for index, row in hasil.iterrows():
                with st.container():
                    st.markdown(f"### 📦 {row['Nama_Produk']}")
                    col1, col2 = st.columns(2)
                    col1.metric("Harga Satuan", f"Rp {row['Harga_Satuan']:,.0f}")
                    col2.metric("Harga Grosir", f"Rp {row['Harga_Grosir']:,.0f}")
                    st.markdown("---")
        else:
            st.warning("Produk tidak ditemukan. Coba kata kunci lain.")
    else:
        st.info("Tips: Ketik merk produk untuk melihat semua varian harganya.")

# Footer bantuan
st.sidebar.title("Bantuan")
st.sidebar.write("Aplikasi ini terhubung langsung dengan sistem SID Retail Pro via Google Sheets.")