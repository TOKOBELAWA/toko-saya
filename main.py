import streamlit as st
import pandas as pd
from PIL import Image
import os

# 1. KONFIGURASI HALAMAN
ICON_FILENAME = "belawa2.PNG" 

if os.path.exists(ICON_FILENAME):
    img = Image.open(ICON_FILENAME)
    st.set_page_config(page_title="Toko Belawa", page_icon=img, layout="centered")
else:
    st.set_page_config(page_title="Toko Belawa", page_icon="🛍️", layout="centered")

# 2. CSS TEMA CREAM
st.markdown("""
    <style>
    .stApp { background-color: #FEFDF5; color: #333333; }
    h1 { text-align: center; color: #F63366 !important; font-weight: bold; }
    .stTextInput > div > div > input { border: 2px solid #F63366; border-radius: 10px; }
    .price-card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; border-left: 5px solid #F63366; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .price-tag { font-size: 32px; font-weight: bold; color: #F63366; }
    </style>
""", unsafe_allow_html=True)

# 3. LOGO & JUDUL
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if os.path.exists(ICON_FILENAME):
        st.image(ICON_FILENAME, width=150)

st.title("Toko Belawa")

# 4. LINK DATA (WAJIB DIISI)
# Pastikan link di bawah ini diawali https:// dan diakhiri output=xlsx
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"

@st.cache_data
def load_data(url):
    try:
        # PENTING: Kode ini akan mengecek apakah link valid
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data(URL)
query = st.text_input("", placeholder="🔍 Ketik nama barang...")

# 5. TAMPIL HASIL
if query:
    if df is not None:
        hasil = df[df['Nama Barang'].str.contains(query, case=False, na=False)]
        if not hasil.empty:
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
    else:
        st.error("Gagal mengambil data. Pastikan link di kode main.py sudah benar.")
