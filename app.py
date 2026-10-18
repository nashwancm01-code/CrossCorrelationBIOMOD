import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cross Correlation App", layout="wide")

st.title("Gait Signal Analysis: Cross Correlation")

# Sidebar untuk upload file
st.sidebar.header("Input Data")
heel_file = st.sidebar.file_uploader("Upload File Heel (txt)", type=["txt"])
toe_file = st.sidebar.file_uploader("Upload File Toe (txt)", type=["txt"])

if heel_file is not None and toe_file is not None:
    # Load data
    x_full = np.loadtxt(heel_file)
    y_full = np.loadtxt(toe_file)

    sample_x = len(x_full) - 1
    sample_y = len(y_full) - 1
    sample = min(sample_x, sample_y)

    x = x_full[:sample + 1]
    y = y_full[:sample + 1]

    # Trackbar untuk menggeser sinyal
    shift = st.slider("Shift Toe Signal (Index)", min_value=0, max_value=7000, value=0, step=1)

    # Menampilkan Grafik Sinyal Awal
    st.subheader("Gait Signal")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(range(len(x)), x, label="Heel (x)", color='red')
    
    x_shifted = np.arange(shift, shift + len(y))
    ax1.plot(x_shifted, y, label="Toe (y)", color='lime')
    ax1.set_xlabel("Sample Number")
    ax1.set_ylabel("Amplitude")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    st.divider()

    if st.button("Hitung Korelasi & Normalisasi"):
        # Menyiapkan array kosong untuk hasil
        Rxy = np.zeros(sample + 1)
        Norm = np.zeros(sample + 1)

        with st.spinner('Menghitung korelasi manual...'):
            # ==============================================================
            # 1. RUMUS KORELASI MANUAL 
            # (Ini murni 100% copy logika Delphi Keanu)
            # Rumus Matematis: Rxy[L] = Sigma (x[n] * y[n - L])
            # ==============================================================
            for L in range(sample + 1):
                sigmaL = 0.0
                for n in range(sample + 1):
                    # Syarat batas index agar tidak error (sama seperti di Delphi)
                    if (n - L >= 0) and (n - L <= sample):
                        sigmaL = sigmaL + (x[n] * y[n - L])
                Rxy[L] = sigmaL

            # ==============================================================
            # 2. RUMUS NORMALISASI MANUAL
            # Rumus Matematis: Norm[L] = Rxy[L] / (sample - L)
            # ==============================================================
            for L in range(sample): 
                Norm[L] = Rxy[L] / (sample - L)
            
            Norm[sample] = 0 # Menghindari pembagian dengan nol di akhir

        # Menampilkan Hasil di Layar
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Cross Correlation")
            fig2, ax2 = plt.subplots(figsize=(8, 3))
            ax2.plot(range(len(Rxy)), Rxy, color='red', label="Rxy")
            ax2.set_xlabel("Index Time Lag (L)")
            ax2.set_ylabel("Rxy Value")
            ax2.grid(True)
            st.pyplot(fig2)

            st.subheader("Normalization")
            fig3, ax3 = plt.subplots(figsize=(8, 3))
            ax3.plot(range(len(Norm)-1), Norm[:-1], color='red', label="Normalization")
            ax3.set_xlabel("Index Time Lag (L)")
            ax3.set_ylabel("Rxy Normalization")
            ax3.grid(True)
            st.pyplot(fig3)

        with col2:
            st.subheader("Data Rxy")
            df_rxy = pd.DataFrame({
                "Lag (L)": range(sample + 1),
                "Rxy Value": np.round(Rxy, 3)
            })
            st.dataframe(df_rxy, height=400)
else:
    st.info("Silakan upload file Heel123.txt dan Toe123.txt di sidebar sebelah kiri.")
