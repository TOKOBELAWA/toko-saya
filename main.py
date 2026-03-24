import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. KONFIGURASI TAMPILAN (Setting Tema Gelap dan Ikon Baru)
# Perubahan penting ada di baris ini
ICON_FILENAME = "belawa.png"

# Memastikan file gambar ikon ada sebelum memakainya
if os.path.exists(ICON_FILENAME):
    img = Image.open(ICON_FILENAME)
    st.set_page_config(
        page_title="Toko Bela Jaya",
        page_icon=img,  # Ikon baru memakai gambar Anda
        layout="centered",
        initial_sidebar_state="collapsed",
    )
else:
    # Jika gambar tidak ketemu di GitHub, pakai ikon default
    st.set_page_config(
        page_title="CEK MANDIRI HARGA BARANG KAMI",
        page_icon="🛍️", # Ikon default
        layout="centered",
    )

# --- CSS KHUSUS UNTUK TEMA GELAP & AKSEN PINK (Mewah & Modern) ---
st.markdown("""
    <style>
    /* Mengubah latar belakang utama menjadi HITAM PEKAT */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA; /* Tulisan putih agar jelas */
    }
    /* Mengubah warna teks judul (st.title) menjadi PINK CERAH */
    h1 {
        text-align: center;
        color: #F63366 !important; /* Warna Pink/Merah Muda */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
    }
    /* Gaya untuk teks instruksi di bawah judul */
    .instruction-text {
        text-align: center;
        color: #B0B0B0; /* Abu-abu muda */
        margin-top: -15px;
        margin-bottom: 25px;
    }
    /* Mengubah warna latar belakang kotak pencarian menjadi ABU-ABU GELAP */
    .stTextInput > div > div > input {
        background-color: #262730; /* Abu-abu tua */
        color: #FAFAFA; /* Tulisan putih di dalam kotak */
        border: 2px solid #4B4D52; /* Bingkai abu-abu */
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
    }
    /* Mengubah warna teks placeholder ("Cari barang...") */
    .stTextInput > div > div > input::placeholder {
        color: #808080; /* Abu-abu redup */
    }
    /* Mengubah gaya kotak hasil harga menjadi kartu modern dengan bayangan */
    .price-card {
        background-color: #1A1D24; /* Kartu abu-abu gelap */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3); /* Efek bayangan */
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
        color: #FAFAFA; /* Putih */
        margin-bottom: 8px;
    }
    /* Gaya untuk footer */
    .footer-text {
        text-align: center;
        color: #808080; /* Abu-abu */
        font-size: 12px;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. JUDUL APLIKASI
# Menampilkan Logo Anda di Atas Judul
if os.path.exists(ICON_FILENAME):
    img_display = Image.open(ICON_FILENAME)
    # Menampilkan logo di tengah
    st.image(img_display, width=150)

st.title("🛒 TOKO BELAWA")
st.markdown("<p class='instruction-text'>Ketik nama barang untuk cek harga</p>", unsafe_allow_html=True)

# === 3. MASUKKAN LINK HASIL PUBLISH TO WEB ANDA DI SINI ===
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

# 4. KOTAK PENCARIAN (Input Teks)
query = st.text_input("", placeholder="🔍 Cari barang... (Contoh: Susu,Makanan,dll)")

# 5. MENAMPILKAN HASIL PENCARIAN
if df is not None and query:
    # Cek apakah kolom yang dibutuhkan ada
    if 'Nama Barang' in df.columns and 'Harga' in df.columns:
        # Cari barang berdasarkan nama (tidak sensitif huruf besar/kecil)
        hasil = df[df['Nama Barang'].str.contains(query, case=False, na=False)]
        
        if not hasil.empty:
            st.markdown("<h3 style='text-align: left; color: #F63366;'>Hasil Pencarian:</h3>", unsafe_allow_html=True)
            for i, row in hasil.iterrows():
                # Menampilkan harga dalam kartu modern
                st.markdown(f"""
                    <div class="price-card">
                        <div class="item-name">📦 {row['Nama Barang']}</div>
                        <div style="color: #B0B0B0; font-size: 14px;">Harga:</div>
                        <div class="price-tag">Rp {row['Harga']:,}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            # Tampilkan peringatan jika barang tidak ditemukan
            st.warning(f"Barang dengan kata kunci '{query}' tidak ditemukan.")
    else:
        st.error("Format data Google Sheets salah. Pastikan ada kolom 'Nama Barang' dan 'Harga' dengan ejaan yang sama.")

# 6. TAMPILAN KAKI (FOOTER)
st.markdown("<p class='footer-text'>Powered by Streamlit | Desain Kustom Toko Bela</p>", unsafe_allow_html=True)
