import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- 1. KONFIGURASI HALAMAN ---
# Nama file ikon sesuai permintaan Anda
ICON_FILENAME = "belawa2.PNG" 

if os.path.exists(ICON_FILENAME):
    img = Image.open(ICON_FILENAME)
    st.set_page_config(page_title="Toko Belawa", page_icon=img, layout="centered")
else:
    st.set_page_config(page_title="Toko Belawa", page_icon="🛍️", layout="centered")

# --- 2. CSS TEMA CREAM CERAH ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FEFDF5;
        color: #333333;
    }
    h1 {
        text-align: center;
        color: #F63366 !important;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        color: #333333;
        border: 2px solid #F63366;
        border-radius: 10px;
    }
    .price-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #F63366;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .price-tag {
        font-size: 32px;
        font-weight: bold;
        color: #F63366;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGO & JUDUL ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists(ICON_FILENAME):
        st.image(ICON_FILENAME, width=150)

st.title("Toko Belawa")
st.markdown("<p style='text-align: center; color: #707070;'>Cek harga barang jadi lebih mudah</p>", unsafe_allow_html=True)

# --- 4. DATA GOOGLE SHEETS (WAJIB GANTI LINK INI) ---
# Masukkan link 'Publish to Web' Anda yang berakhiran output=xlsx di bawah ini:
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_excel(url)
        # Bersihkan nama kolom dari spasi yang tidak sengaja terketik
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data(URL)
query = st.text_input("", placeholder="🔍 Ketik nama barang...")

# --- 5. LOGIKA TAMPIL HARGA ---
if df is not None and query:
    # Mencari di kolom 'Nama Barang'
    hasil = df[df['Nama Barang'].str.contains(query, case=False, na=False)]
    
    if not hasil.empty:
        st.markdown("<h3 style='color: #F63366;'>Hasil:</h3>", unsafe_allow_html=True)
        for i, row in hasil.iterrows():
            st.markdown(f"""
                <div class="price-card">
                    <div style="font-size: 20px; font-weight: bold;">📦 {row['Nama Barang']}</div>
                    <div style="color: #707070;">Harga:</div>
                    <div class="price-tag">Rp {row['Harga']:,}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"Barang '{query}' tidak ditemukan.")
elif df is None:
    st.error("Data tidak terbaca. Pastikan link Google Sheets sudah benar dan sudah di-Publish to Web.")
