import streamlit as st
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Scanner Harga SID Retail",
    page_icon="🛒",
    layout="centered"
)

# CSS Custom untuk tampilan Mobile-Friendly
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNGSI AMBIL DATA (DATA ENGINE) ---
@st.cache_data(ttl=60) # Cache selama 1 menit agar data tetap segar
def load_data_from_gsheets():
    # GANTI URL ini dengan Link 'Publish to Web' format XLSX dari Google Sheets Anda
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyWz8RRE9o3sI9Ab-xQXswT6q2ztO4kzqKF8JNGmKZi_IDBC5a2nI8ByuXxkh6NaaspPbstncGDbH4/pub?output=xlsx"
    
    try:
        # Membaca file excel dari URL
        df = pd.read_excel(URL)
        
        # --- PERBAIKAN BARCODE (Leading Zeros) ---
        # 1. Pastikan kolom Barcode adalah string
        # 2. Hapus spasi jika ada
        # 3. Gunakan .zfill(3) jika barcode Anda standar 3 digit (Ganti angka 3 sesuai kebutuhan)
        df['Barcode'] = df['Barcode'].astype(str).str.strip().str.replace('.0', '', regex=False)
        
        # Opsional: Jika barcode Anda panjangnya bervariasi (misal ada yang 3 digit, ada yang 13 digit),
        # pastikan format di Google Sheets adalah 'Plain Text'.
        
        return df
    except Exception as e:
        st.error(f"Koneksi Gagal: {e}")
        return None

# Memanggil data
df_produk = load_data_from_gsheets()

# --- 3. ANTARMUKA PENGGUNA (UI) ---
st.title("🛒 Cek Harga Mandiri")
st.info("Silakan scan barcode produk atau cari berdasarkan nama.")

if df_produk is not None:
    # TAB MENU: Scan vs Cari Manual
    tab_scan, tab_cari = st.tabs(["📷 Scan Barcode", "🔍 Cari Nama"])

    with tab_scan:
        try:
            from streamlit_barcode_scanner import st_barcode_scanner
            st.write("Arahkan kamera ke Barcode produk:")
            scan_val = st_barcode_scanner()

            if scan_val:
                # Normalisasi hasil scan
                kode_scan = str(scan_val).strip()
                
                # Pencarian di DataFrame
                hasil = df_produk[df_produk['Barcode'] == kode_scan]
                
                if not hasil.empty:
                    p = hasil.iloc[0]
                    st.success(f"### {p['Nama_Produk']}")
                    col1, col2 = st.columns(2)
                    col1.metric("Harga Satuan", f"Rp {p['Harga_Satuan']:,.0f}")
                    col2.metric("Harga Grosir", f"Rp {p['Harga_Grosir']:,.0f}")
                else:
                    st.error(f"Barcode '{kode_scan}' tidak ditemukan.")
        except Exception:
            st.warning("Gagal memuat modul kamera. Gunakan tab 'Cari Nama'.")

    with tab_cari:
        input_nama = st.text_input("Ketik nama produk:", placeholder="Contoh: Sunsilk").strip()
        
        if input_nama:
            # Cari nama yang mirip (case insensitive)
            search_res = df_produk[df_produk['Nama_Produk'].str.contains(input_nama, case=False, na=False)]
            
            if not search_res.empty:
                for idx, row in search_res.iterrows():
                    with st.expander(f"📦 {row['Nama_Produk']} (ID: {row['Barcode']})"):
                        c1, c2 = st.columns(2)
                        c1.metric("Satuan", f"Rp {row['Harga_Satuan']:,.0f}")
                        c2.metric("Grosir", f"Rp {row['Harga_Grosir']:,.0f}")
            else:
                st.error("Produk tidak ditemukan.")

else:
    st.error("Database tidak dapat diakses. Pastikan Link Google Sheets sudah benar.")

# --- FOOTER ---
st.divider()
st.caption("Aplikasi Terhubung dengan Database SID Retail Pro via Google Sheets.")
