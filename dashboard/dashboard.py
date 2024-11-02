import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for seaborn
sns.set_style("whitegrid")

# Judul Aplikasi
st.title("Analisis Data Kualitas Udara")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Tentang Dataset", "Data Wrangling", "Cleaning Data", "Exploratory Data Analysis", "Visualisasi"])

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data = pd.read_csv('./data/PRSA_Data_Shunyi_20130301-20170228.csv')
    # Menggabungkan kolom waktu
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])

    # Menetapkan datetime sebagai index
    data.set_index('datetime', inplace=True)

    # Menghapus kolom yang tidak perlu
    data.drop(columns=['year', 'month', 'day', 'hour', 'No', 'station'], inplace=True)

    # Menghapus outlier
    Q1 = data['PM2.5'].quantile(0.25)
    Q3 = data['PM2.5'].quantile(0.75)
    IQR = Q3 - Q1
    data = data[~((data['PM2.5'] < (Q1 - 1.5 * IQR)) | (data['PM2.5'] > (Q3 + 1.5 * IQR)))]

    data['day_of_week'] = data.index.day_name()
    data['is_weekend'] = data['day_of_week'].isin(['Saturday', 'Sunday'])
    data['season'] = data.index.month % 12 // 3 + 1
    data['season_label'] = data['season'].map({1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})
    data['humidity_level'] = pd.cut(data['DEWP'], bins=[-np.inf, 0, 10, np.inf], labels=['Low', 'Medium', 'High'])
    return data

# Memuat data
data = load_data()

# Variabel
yearly_avg = data.resample('YE')['PM2.5'].mean()
weekend_avg = data.groupby('is_weekend')['PM2.5'].mean()
hourly_avg = data.groupby(data.index.hour)['PM2.5'].mean()
seasonal_avg = data.groupby('season_label')['PM2.5'].mean()
humidity_avg = data.groupby('humidity_level', observed=False)['PM2.5'].mean()

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
    
    # Mengecek jumlah missing values
    missing_values = data.isnull().sum()
    st.write(missing_values)

    # Membuat dataframe untuk visualisasi
    missing_df = pd.DataFrame({
        'Missing Values': missing_values
    })

    # Menyaring kolom yang memiliki missing values
    missing_df = missing_df[missing_df['Missing Values'] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    missing_df.sort_values(by='Missing Values', ascending=False, inplace=True)
    missing_df['Missing Values'].plot(kind='bar', color='steelblue')
    ax.set_title('Jumlah Missing Values per Kolom')
    ax.set_xlabel('Kolom')
    ax.set_ylabel('Jumlah Missing Values')
    # ax.set_xticklabels(missing_df.index, rotation=45)
    st.pyplot(fig)

    st.write("""
Insight:
- Beberapa kolom memiliki missing values, terutama pada kolom PM2.5 dan PM10, yang perlu ditangani
- Data waktu (tahun, bulan, hari, dan jam) perlu dikombinasikan untuk analisis tren""")

# 3. Cleaning Data
elif page == "Cleaning Data":
    st.header("Cleaning Data")
    st.subheader("Data yang sudah di bersihkan")
    st.write(data.describe())
    st.write("""
Insight:
- Data telah dibersihkan dengan menggabungkan kolom waktu dan mengisi nilai yang hilang dengan rata-rata
- Penghapusan outlier""")

# 4. Exploratory Data Analysis (EDA)
elif page == "Exploratory Data Analysis":
    # Melihat distribusi data PM2.5
    st.header("Exploratory Data Analysis")
    st.subheader("1. Explore Data Distribusi PM2.5 Tahunan")
    st.write(yearly_avg)

    st.subheader("2. Explore Data Hubungan Suhu dan PM2.5")
    st.write(data[['PM2.5', 'TEMP']].corr())

    st.subheader("3. Explore Variasi Hari Kerja vs Akhir Pekan")
    st.write(weekend_avg)

    st.subheader("4. Expoler Data Variasi Harian")
    st.write(hourly_avg)

    st.subheader("5. Explore Pola Data Musiman")
    st.write(seasonal_avg)

    st.subheader("6. Explore Data Kelembaban")
    st.write(humidity_avg)
    
    st.subheader("7. Explore distribusi data PM2.5")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['PM2.5'], bins=30, kde=True, ax=ax)
    ax.set_title('Distribusi PM2.5')
    ax.set_xlabel('Konsentrasi PM2.5')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)

# 5. Visualisasi
elif page == "Visualisasi":
    st.header("Visualisasi Hubungan Faktor Lingkungan dengan PM2.5")

    st.subheader("Pertanyaan 1: Bagaimana distribusi tahunan dan tren jangka panjang PM2.5 selama periode 2013-2017?")
    fig, ax = plt.subplots(figsize=(10, 6))
    yearly_avg.plot(kind='bar', color='lightblue')
    ax.set_title('Rata-rata PM2.5 Tahunan (2013-2017)')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('PM2.5 (µg/m³)')
    # ax.set_xticklabels(rotation=45)
    st.pyplot(fig)

    st.subheader("Pertanyaan 2: Bagaimana faktor suhu mempengaruhi konsentrasi PM2.5 selama periode tersebut?")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x='TEMP', y='PM2.5', data=data, alpha=0.5, hue='TEMP', palette='coolwarm')
    ax.set_title('Hubungan Suhu dan PM2.5')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('PM2.5 (µg/m³)')
    st.pyplot(fig)

    st.subheader("Pertanyaan 3: Bagaimana variasi konsentrasi PM2.5 antara hari kerja dan akhir pekan?")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='is_weekend', y='PM2.5', data=data, hue='is_weekend', palette='Set2', legend=False)
    ax.set_title('Distribusi PM2.5: Hari Kerja vs Akhir Pekan')
    ax.set_xlabel('Akhir Pekan')
    ax.set_ylabel('PM2.5 (µg/m³)')
    # ax.set_xticklabels([0, 1], ['Hari Kerja', 'Akhir Pekan'])
    st.pyplot(fig)

    st.subheader("Pertanyaan 4: Apakah ada perbedaan signifikan konsentrasi PM2.5 pada jam tertentu sepanjang hari?")
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_avg.plot(kind='line', marker='o', color='orange')
    ax.set_title('Rata-rata PM2.5 per Jam dalam Sehari')
    ax.set_xlabel('Jam')
    ax.set_ylabel('PM2.5 (µg/m³)')
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("Pertanyaan 5: Bagaimana perbandingan variasi PM2.5 pada setiap musim?")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='season_label', y='PM2.5', data=data, hue='season_label', palette='muted', dodge=False, legend=False)
    ax.set_title('Distribusi PM2.5 Berdasarkan Musim')
    ax.set_xlabel('Musim')
    ax.set_ylabel('PM2.5 (µg/m³)')
    st.pyplot(fig)

    st.subheader("Pertanyaan 6: Bagaimana tren kualitas udara (PM2.5) di wilayah Shunyi selama periode 2013-2017?")
    fig, ax = plt.subplots(figsize=(12, 6))
    # Mengelompokkan data berdasarkan bulan untuk mendapatkan rata-rata PM2.5
    monthly_avg_pm25 = data['PM2.5'].resample('ME').mean().reset_index()

    sns.lineplot(x='datetime', y='PM2.5', data=monthly_avg_pm25, marker='o', color='blue')
    ax.set_title('Tren Rata-rata Bulanan Kualitas Udara (PM2.5) di Wilayah Shunyi (2013-2017)')
    ax.set_xlabel('Waktu (Bulan)')
    ax.set_ylabel('Rata-rata PM2.5 (µg/m³)')
    # ax.set_xticklabels(rotation=45)
    st.pyplot(fig)

    st.write("""
Insight:
- Data menunjukan tren konsentrasi PM2.5 berubah setiap tahun.
- Dapat melihat pola konsentrasi PM2.5 yang cenderung naik atau turun dengan suhu tertentu.
- Dapat membantu memahami konsentrasi PM2.5 yang memiliki perbedaan signifikan antara hari kerja dan akhir pekan.
- Dapat membantu melihat pada jam-jam tertentu dalam sehari di mana polusi udara cenderung lebih tinggi.
- Dapat memberikan gambaran variasi konsentrasi PM2.5 antara musim yang berbeda.
- Tren data menunjukkan adanya peningkatan atau penurunan polutan pada waktu-waktu tertentu, menunjukkan potensi adanya pola musiman.""")

    # Clustering
    st.header("Clustering Analisis")

    st.subheader("Berdasarkan Tingkat Polusi PM2.5")

    # Kategori clustering berdasarkan rentang nilai
    def pm25_clustering(value):
        if value < 35:
            return 'Good'
        elif 35 <= value < 75:
            return 'Moderate'
        else:
            return 'Unhealthy'

    # Buat kolom cluster pada dataset
    data['PM2.5 Cluster'] = data['PM2.5'].apply(pm25_clustering)

    # Plot visualisasi distribusi cluster
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.countplot(x='PM2.5 Cluster', data=data, hue='PM2.5 Cluster', dodge=False, palette='coolwarm')
    ax.set_title('Distribusi Clustering PM2.5')
    ax.set_xlabel('Kategori Clustering')
    ax.set_ylabel('Jumlah Observasi')
    st.pyplot(fig)

    st.subheader("Analisis Distribusi Polusi Berdasarkan Faktor Lingkungan")
    # Visualisasi rata-rata PM2.5 berdasarkan level kelembapan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=humidity_avg.index, y=humidity_avg.values, hue=humidity_avg.index, palette='coolwarm', dodge=False)
    ax.set_title('Rata-rata PM2.5 Berdasarkan Level Kelembapan')
    ax.set_xlabel('Level Kelembapan')
    ax.set_ylabel('PM2.5 (µg/m³)')
    # ax.set_xticklabels('Level Kelembapan', rotation=45)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    scatter = sns.scatterplot(x='WSPM', y='PM2.5', data=data, alpha=0.6, hue='WSPM', palette='coolwarm', ax=ax)
    norm = plt.Normalize(data['WSPM'].min(), data['WSPM'].max())
    sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label='Kecepatan Angin (WSPM)')
    ax.set_title('Hubungan antara Kecepatan Angin (WSPM) dan Konsentrasi PM2.5')
    ax.set_xlabel('Kecepatan Angin (m/s)')
    ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)')
    st.pyplot(fig)