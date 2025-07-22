import streamlit as st
import pandas as pd
from statsmodels.tsa.stattools import kpss
import numpy as np


# -- Fungsi untuk melakukan Tes KPSS --

def kpss_test(timeseries, regression_type, nlags_param):
    """
    Melakukan Tes KPSS pada data time series.
    """
    try:
        # Menggunakan parameter nlags_param yang diberikan
        kpss_stat, p_value, lags, crit = kpss(timeseries, regression=regression_type, nlags=nlags_param)
        return kpss_stat, p_value, lags, crit
    except Exception as e:
        st.error(f"Terjadi error saat melakukan tes KPSS: {e}")
        return None, None, None, None


# -- Konfigurasi Halaman Streamlit --
st.set_page_config(
    page_title="Aplikasi Tes KPSS",
    page_icon="📊",
    layout="centered"
)

# -- Judul dan Deskripsi Aplikasi --
st.title("📊 Aplikasi Uji Stasioneritas KPSS")
st.markdown("""
Aplikasi ini melakukan uji **Kwiatkowski-Phillips-Schmidt-Shin (KPSS)** pada data time series Anda.
Uji KPSS digunakan untuk menguji hipotesis nol bahwa data time series adalah stasioner.
""")
st.markdown("---")

# --  Unggah File CSV --
st.header("Unggah Data Time Series Anda")
uploaded_file = st.file_uploader("Pilih file CSV", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("File CSV berhasil diunggah!")
        st.write("**Pratinjau Data:**")
        st.dataframe(data.head())

        # --  Pilih Kolom dan Parameter Tes --
        st.header("Konfigurasi Tes")

        available_columns = data.columns.tolist()
        selected_column = st.selectbox("Pilih kolom time series:", available_columns)

        regression_type = st.radio(
            "Pilih hipotesis stasioneritas:",
            ('c', 'ct'),
            format_func=lambda
                x: "Stasioner di sekitar rata-rata (Level Stationary)" if x == 'c' else "Stasioner di sekitar tren (Trend Stationary)"
        )

        # <<< BARU: Menambahkan opsi untuk mengatur parameter lag secara manual >>>
        st.subheader("Pengaturan Jumlah Lag (nlags)")
        nlags_option = st.radio(
            "Pilih metode penentuan lag:",
            ('Otomatis', 'Manual'),
            key='nlags_option'
        )

        lags_to_use = "auto"  # Nilai default
        if nlags_option == 'Manual':
            # Rumus Schwert sebagai rekomendasi
            recommended_lags = int(12 * (len(data) / 100) ** 0.25)
            manual_lags = st.number_input(
                "Masukkan jumlah lag:",
                min_value=0,
                value=recommended_lags,
                step=1,
                help=f"Rekomendasi umum (formula Schwert) untuk data Anda adalah: {recommended_lags}"
            )
            lags_to_use = manual_lags
        # <<< AKHIR BAGIAN BARU >>>

        # -- Jalankan Tes --
        if st.button("Jalankan Tes KPSS", key="run_test"):
            if selected_column:
                # Menghilangkan koma dan mengubah tipe data, serta menghapus nilai kosong
                cleaned_series = pd.to_numeric(data[selected_column].astype(str).str.replace(',', ''), errors='coerce')
                timeseries = cleaned_series.dropna()

                if len(timeseries) < 10:
                    st.warning("Data time series terlalu pendek. Hasil tes mungkin tidak akurat.")
                else:
                    with st.spinner("Melakukan tes..."):
                        # Memanggil fungsi dengan parameter lag yang sudah dipilih
                        kpss_stat, p_value, lags, crit = kpss_test(timeseries, regression_type, lags_to_use)

                        if kpss_stat is not None:
                            # -- Hasil --
                            st.header("Hasil Tes KPSS")
                            st.write(f"**Kolom yang Diuji:** `{selected_column}`")
                            st.write(f"**Metode Lag:** `{nlags_option}`")

                            col1, col2, col3 = st.columns(3)
                            col1.metric("Statistik KPSS", f"{kpss_stat:.4f}")
                            col2.metric("P-value", f"{p_value:.4f}")
                            col3.metric("Jumlah Lag yang Digunakan", lags)

                            st.subheader("Interpretasi")
                            alpha = 0.05
                            # Untuk KPSS, hipotesis nol adalah stasioneritas.
                            # Jika p-value < alpha, kita tolak H0, berarti data TIDAK stasioner.
                            if p_value < alpha:
                                st.error(
                                    f"**Kesimpulan: Hipotesis nol ditolak (p-value < {alpha}).** Data kemungkinan besar **TIDAK STASIONER**.")
                            else:
                                st.success(
                                    f"**Kesimpulan: Gagal menolak hipotesis nol (p-value >= {alpha}).** Data kemungkinan besar **STASIONER**.")

                            with st.expander("Lihat Nilai Kritis"):
                                st.write(
                                    "Nilai kritis digunakan untuk membandingkan dengan statistik KPSS pada tingkat signifikansi yang berbeda:")
                                st.json(crit)

    except Exception as e:
        st.error(f"Gagal memproses file CSV. Error: {e}")

else:
    st.info("Silakan unggah file CSV untuk memulai.")