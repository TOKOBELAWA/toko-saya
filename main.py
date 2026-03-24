import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- 1. KONFIGURASI HALAMAN & IKON ---
# Memakai logo Anda sebagai ikon di tab browser
ICON_FILENAME = "belawa2.png"

if os.path.exists(ICON_FILENAME):
    img = Image.open(ICON_FILENAME)
    st.set_page_config(
        page_title="Toko Belawa",
        page_icon=img, 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
else:
    st.set_page_config(
        page_title="Toko Belawa",
        page_icon="🛍️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

# --- 2. CSS TEMA CERAH (Cream & Pink) ---
st.markdown("""
    <style>
    /* Mengubah latar belakang utama menjadi WARNA CREAM */
    .stApp {
        background-color: #FEFDF5; /* Warna Cream Lembut */
        color: #333333; /* Tulisan abu-abu tua agar tidak kaku */
    }
    /* Mengubah warna teks judul (st.title) menjadi PINK CERAH */
    h1 {
        text-align: center;
        color: #F63366 !important; /* Warna Pink/Merah Muda Anda */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
        margin-top: -10px;
    }
    /* Gaya untuk teks instruksi di bawah judul */
    .instruction-text {
        text-align: center;
        color: #707070; /* Abu-abu tua */
        margin-top: -15px;
        margin-bottom: 25px;
        font-size: 16px;
    }
    /* Mengubah warna kotak pencarian menjadi PUTIH dengan bingkai PINK */
    .stTextInput > div > div > input {
        background-color: #FFFFFF; /* Putih bersih */
        color: #333333;
        border: 2px solid #F63366; /* Bingkai Pink */
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    /* Mengubah warna teks placeholder ("Ketik nama barang...") */
    .stTextInput > div > div > input::placeholder {
        color: #B0B0B0; /* Abu-abu muda */
    }
    /* Mengubah gaya kotak hasil harga menjadi kartu PUTIH modern */
    .price-card {
        background-color: #FFFFFF; /* Kartu Putih bersih */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05); /* Bayangan sangat halus */
        border-left: 5px solid #F63366; /* Garis vertikal pink di kiri */
    }
    /* Mengubah gaya teks harga menjadi besar, bold, dan PINK */
    .price-tag {
        font-size: 36px;
        font-weight: bold;
        color: #F63366; /* Pink cerah */
        margin-top: 5px;
    }
    /* Gaya untuk nama barang */
    .item-name {
        font-size: 22px;
        font-weight: bold;
        color: #333333; /* Abu-abu tua */
        margin-bottom: 8px;
    }
    /* Gaya untuk footer */
    .footer-text {
        text-align: center;
        color: #A0A0A0; /* Abu-abu muda */
        font-size: 12px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. TAMPILAN LOGO & JUDUL ---
# Menampilkan Logo Anda di Atas Judul, ditaruh di tengah
col1, col2, col3 = st.columns([1, 1, 1])
with col2: # Kolom tengah
    if os.path.exists(ICON_FILENAME):
        st.image(ICON_FILENAME, width=150)

st.title("Cek Harga Di Sini")
st.markdown("<p class='instruction-text'>Cek harga barang jadi lebih mudah</p>", unsafe_allow_html=True)

# === 4. DATA GOOGLE SHEETS ===
# === GANTI LINK DI BAWAH INI DENGAN LINK 'PUBLISH TO WEB' ANDA ===
# Harus berakhiran pub?output=xlsx
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"
# =======================================================

@st.cache_data # Cache data agar aplikasi cepat
def load_data(url):
    try:
        # Menambahkan parameter Excel untuk memastikan formatnya Excel
        url_excel = url
        if "?output=xlsx" not in url:
            url_excel = url + "&output=xlsx"
        
        # Membaca file Excel dari link
        df = pd.read_excel(url_excel)
        # Menghapus spasi di awal/akhir nama kolom
        df.columns = df.columns.str.strip()
        
        # Memastikan kolom 'Harga' adalah angka
        if 'Harga' in df.columns:
            df['Harga'] = pd.to_numeric(df['Harga'], errors='coerce')
            
        return df
    except Exception as e:
        # Menampilkan error jika gagal memuat data
        st.error(f"Gagal menyambung ke data Google Sheets. Error: {e}")
        return None

# Panggil fungsi muat data
df = load_data(URL)

# --- 5. KOTAK PENCARIAN (Input Teks) ---
# Dibuat tanpa label di atasnya, placeholder lebih jelas
query = st.text_input("", placeholder="🔍 Ketik nama barang...")

# --- 6. MENAMPILKAN HASIL PENCARIAN ---
if df is not None and query:
    # Cek apakah kolom yang dibutuhkan ada
    if 'Nama Barang' in df.columns and 'Harga' in df.columns:
        # Cari barang berdasarkan nama (tidak sensitif huruf besar/kecil)
        hasil = df[df['Nama Barang'].str.contains(query, case=False, na=False)]
        
        if not hasil.empty:
            st.markdown("<h3 style='text-align: left; color: #F63366; margin-top: 20px;'>Hasil Pencarian:</h3>", unsafe_allow_html=True)
            for i, row in hasil.iterrows():
                # Menampilkan harga dalam kartu putih modern dengan desain bersih
                st.markdown(f"""
                    <div class="price-card">
                        <div class="item-name">📦 {row['Nama Barang']}</div>
                        <div style="color: #707070; font-size: 14px;">Harga:</div>
                        <div class="price-tag">Rp {row['Harga']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Tampilkan peringatan jika barang tidak ditemukan
            st.warning(f"Barang dengan kata kunci '{query}' tidak ditemukan.")
    else:
        st.error("Format data Google Sheets salah. Pastikan ada kolom 'Nama Barang' dan 'Harga' dengan ejaan yang sama.")

# --- 7. TAMPILAN KAKI (FOOTER) ---
st.markdown("<p class='footer-text'>Powered by Streamlit |TOKO BELAWA TANRUTEDONG</p>", unsafe_allow_html=True)
