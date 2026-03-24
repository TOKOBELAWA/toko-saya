import streamlit as st
import pandas as pd

# Setting dasar agar tampilan bagus di HP
st.set_page_config(page_title="Cek Harga Toko Belawa", page_icon="🛍️")

# CSS untuk tema gelap dan harga yang mencolok
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stTextInput > div > div > input { background-color: #262730; color: #FAFAFA; border-radius: 10px; }
    h1 { text-align: center; color: #F63366; }
    .price-box { background-color: #1A1D24; padding: 20px; border-radius: 15px; border-left: 5px solid #F63366; margin-bottom: 10px; }
    .price-tag { font-size: 28px; font-weight: bold; color: #00FF00; }
    </style>
""", unsafe_allow_html=True)

st.title("🛒 Toko Belawa")
st.write("<p style='text-align: center;'>Ketik nama barang untuk cek harga</p>", unsafe_allow_html=True)

# MASUKKAN LINK HASIL PUBLISH TO WEB ANDA DI SINI
# Harus berakhiran pub?output=xlsx
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vThtKCMQU9bIxl5jxsbfMKtX3B6zyRYwxuNcX4xSRzFugE4uBvj8btRryLEUgql-SDWkIvJ7Q4Wu0ih/pub?output=xlsx"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_excel(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

df = load_data(URL)
query = st.text_input("", placeholder="🔍 Cari barang... (Contoh: Susu, Minuman,Sabun, Bedak, dll)")

if df is not None and query:
    # Mencari di kolom 'Nama Barang'
    hasil = df[df['Nama Barang'].str.contains(query, case=False, na=False)]
    
    if not hasil.empty:
        for i, row in hasil.iterrows():
            st.markdown(f"""
                <div class="price-box">
                    <div style="font-size: 18px;">📦 {row['Nama Barang']}</div>
                    <div class="price-tag">Rp {row['Harga']:,}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Barang tidak ditemukan.")
elif df is None:
    st.error("Gagal menyambung ke data. Cek kembali link Google Sheets Anda.")
