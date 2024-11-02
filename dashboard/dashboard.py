import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Aplikasi
st.title("Analisis Data Kualitas Udara")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Tentang Dataset", "Data Wrangling", "Exploratory Data Analysis", "Visualisasi"])

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data = pd.read_csv('./data/PRSA_Data_Shunyi_20130301-20170228.csv')
    # Menggabungkan kolom waktu
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])

    # Menghapus kolom yang tidak perlu
    data.drop(columns=['year', 'month', 'day', 'hour', 'No', 'station'], inplace=True)
    return data

# Memuat data
data = load_data()

# 1. Tentang Dataset
if page == "Tentang Dataset":
    st.header("Tentang Dataset")
    st.write("Dataset ini berisi data kualitas udara dari 2013 hingga 2017, termasuk informasi polutan (PM2.5, PM10, SO2, NO2, CO, O3) dan faktor lingkungan lainnya.")
    st.write("Jumlah baris dan kolom dataset:", data.shape)
    st.write(data.head())

# 2. Data Wrangling
elif page == "Data Wrangling":
    st.header("Data Wrangling")
    st.subheader("Mengatasi Missing Values")
    st.write("Jumlah missing values pada setiap kolom:")
    st.write(data.isnull().sum())
    st.write("Missing values telah diisi dengan rata-rata dari setiap kolom.")

# 3. Exploratory Data Analysis (EDA)
elif page == "Exploratory Data Analysis":
    # Melihat distribusi data PM2.5
    st.header("Exploratory Data Analysis")
    st.subheader("Distribusi PM2.5")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['PM2.5'], bins=30, kde=True, ax=ax)
    ax.set_title('Distribusi PM2.5')
    ax.set_xlabel('Konsentrasi PM2.5')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)

# 4. Visualisasi
elif page == "Visualisasi":
    st.header("Visualisasi Hubungan Faktor Lingkungan dengan PM2.5")

    # Scatter plot hubungan antara PM2.5 dan suhu
    st.subheader("Hubungan PM2.5 dengan Suhu")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='TEMP', y='PM2.5', data=data, ax=ax)
    ax.set_title('Hubungan PM2.5 dengan Suhu')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Konsentrasi PM2.5')
    st.pyplot(fig)

    # Line plot untuk tren PM2.5
    st.subheader("Tren Kualitas Udara (PM2.5) dari Waktu ke Waktu")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(x='datetime', y='PM2.5', data=data, ax=ax)
    ax.set_title('Tren Kualitas Udara (PM2.5) dari Waktu ke Waktu')
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Konsentrasi PM2.5')
    st.pyplot(fig)
