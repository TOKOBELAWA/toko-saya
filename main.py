import streamlit as st
import pandas as pd

# 1. KONFIGURASI TAMPILAN
st.set_page_config(
    page_title="Silahkan Cek Sendiri Harga Barang Yang Anda Inginkan",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Gaya CSS Kustom untuk Tampilan Gelap Total dan Desain Kartu
st.markdown("""
    <style>
    /* Mengubah warna latar belakang utama */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    /* Mengubah warna latar belakang kotak input */
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
        border-color: #4B4D52;
        border-radius: 10px;
        padding: 12px;
    }
    /* Mengubah warna teks judul */
    h1, h2, h3 {
        color: #FAFAFA !important;
        text-align: center;
    }
    /* Mengubah gaya kotak hasil (expander) */
    .streamlit-expanderHeader {
        background-color: #1A1D24;
        border-radius: 10px;
        margin-bottom: 5px;
        color: #FAFAFA !important;
    }
    /* Mengubah gaya teks harga */
    .big-price {
        font-size: 24px;
        font-weight: bold;
        color: #F63366; /* Warna Tombol Pink/Merah */
    }
    </style>
""", unsafe_allow_html=True)

# 2. JUDUL APLIKASI
st.markdown("<h1 style='font-size: 40px;'>🛒 Silahkan Cek Sendiri Harga Barang Yang Anda Inginkan</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: gray;'>Cetik nama barang di bawah ini untuk melihat harga.</p>", unsafe_allow_html=True)

# 3. KOTAK PENCARIAN NAMA BARANG
# Input teks yang besar dan menonjol
nama_barang_input = st.text_input("", placeholder="🔍 Ketik nama barang (misal: Beras, Mie, Susu)")

# 4. MEMUAT DATA DARI GOOGLE SHEETS
# === GANTI LINK DI BAWAH INI DENGAN LINK GOOGLE SHEETS ANDA ===
URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"
# =============================================================

@st.cache_data # Cache agar tidak download data terus-menerus
def muat_data(url):
    try:
        # Menambahkan parameter untuk memastikan formatnya adalah Excel
        url_format = url
        if "?output=xlsx" not in url:
            url_format = url + "&output=xlsx"
        df = pd.read_excel(url_format)
        
        # Membersihkan spasi di nama kolom
        df.columns = df.columns.str.strip()
        
        # Memastikan harga dalam format angka
        if 'Harga' in df.columns:
            df['Harga'] = pd.to_numeric(df['Harga'], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Gagal memuat data. Pastikan link Google Sheets Anda benar. Error: {e}")
        return None

# Panggil fungsi muat data
df_harga = muat_data(https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx)

# 5. LOGIKA PENCARIAN (Menampilkan Hasil)
if df_harga is not None:
    # Cek apakah kolom yang dibutuhkan ada
    if 'Nama Barang' in df_harga.columns and 'Harga' in df_harga.columns:
        # Jika user mengetik sesuatu
        if nama_barang_input:
            # Cari barang berdasarkan nama (tidak sensitif huruf besar/kecil)
            hasil = df_harga[df_harga['Nama Barang'].str.contains(nama_barang_input, case=False, na=False)]
            
            # Tampilkan hasil dalam bentuk kartu yang rapi
            if not hasil.empty:
                st.markdown("<h3 style='text-align: left; color: #F63366;'>Hasil Pencarian:</h3>", unsafe_allow_html=True)
                for index, row in hasil.iterrows():
                    with st.expander(f"📦 {row['Nama Barang']}", expanded=True):
                        st.write(f"🏷️ **Harga:**")
                        st.markdown(f"<span class='big-price'>Rp {row['Harga']:,}</span>", unsafe_allow_html=True)
                        st.write(f"---")
            else:
                st.warning(f"Barang '{nama_barang_input}' tidak ditemukan.")
    else:
        st.error("Format data Google Sheets salah. Pastikan ada kolom 'Nama Barang' dan 'Harga'.")

# 6. TAMPILAN KAKI (FOOTER)
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Streamlit</p>", unsafe_allow_html=True)
