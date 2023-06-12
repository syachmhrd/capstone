import streamlit as st
import pandas as pd
import altair as alt
from numerize import numerize

st.set_page_config(
    page_title = 'Penanganan Sampah di Indonesia',
    layout='wide'
)

capaian = pd.read_csv('https://drive.google.com/uc?export=download&id=1x6xWf66ngrxyfWb1fneIejI9dq_LmBWb')

st.title("Penanganan Sampah di Indonesia")
st.caption("Oleh: Syach Riyan Muhammad Ardiyansyah")

url = 'https://drive.google.com/uc?export=download&id=1tmg0CbCJm477d0M2OLn-bGHFP0pkqAod'
st.image(url, caption='Berita Tentang Sampah, https://nationalgeographic.grid.id/',use_column_width=True)

st.write("Sampah merupakan salah satu masalah yang terus di hadapi oleh setiap negara, tak terkecuali di Indonesia. Banyak upaya yang dilakukan oleh pemerintah maupun para relawan untuk mengurangi jumlah sampah yang ada. Berdasarkan informasi dari katadata, pada 2021 Indonesia masuk sebagai 5 besar negara penyumbang limbah plastik terbanyak ke lautan, tentunya hal tersebut harus menjadi perhatian bagi seluruh pihak untuk bisa mengurangi produksi sampah. Lalu bagaimana pengelolaan sampah di Indonesia? Apakah sudah cukup baik?")

data1 = pd.pivot_table(
    data= capaian,
    index= 'Tahun',
    aggfunc={
        'Timbulan Sampah Tahunan (ton/tahun)(A)':'sum'
    }
).reset_index()

st.header("Timbulan Sampah 2019 - 2022")

met_2020, met_2021, met_2022 = st.columns(3)

with met_2020:
    curr_trash1 = data1.loc[data1['Tahun']==2020, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    prev_trash1 = data1.loc[data1['Tahun']==2019, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    dif_sum1 = 100*(curr_trash1-prev_trash1)/prev_trash1
    st.metric("Timbulan Sampah 2020", value= numerize.numerize(curr_trash1),delta=f'{dif_sum1:.2f}%')

with met_2021:
    curr_trash2 = data1.loc[data1['Tahun']==2021, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    prev_trash2 = data1.loc[data1['Tahun']==2020, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    dif_sum2 = 100*(curr_trash2-prev_trash2)/prev_trash2
    st.metric("Timbulan Sampah 2021", value= numerize.numerize(curr_trash2),delta=f'{dif_sum2:.2f}%')

with met_2022:
    curr_trash3 = data1.loc[data1['Tahun']==2022, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    prev_trash3 = data1.loc[data1['Tahun']==2021, 'Timbulan Sampah Tahunan (ton/tahun)(A)'].values[0]
    dif_sum3 = 100*(curr_trash3-prev_trash3)/prev_trash3
    st.metric("Timbulan Sampah 2022", value= numerize.numerize(curr_trash3),delta=f'{dif_sum3:.2f}%')

data_coba = pd.pivot_table(
    data= capaian[capaian['Tahun']!=2018],
    index= 'Tahun',
    aggfunc={
        'Timbulan Sampah Tahunan (ton/tahun)(A)':'sum'
    }
).reset_index()

data_coba['Tahun'] = data_coba['Tahun'].astype(str)

trend_line = alt.Chart(data_coba).mark_line().encode(
    alt.X('Tahun', title='Tahun'),
    alt.Y('Timbulan Sampah Tahunan (ton/tahun)(A)', title='Timbulan Sampah', aggregate='sum')
)
st.altair_chart(trend_line,use_container_width=True)

st.write("Berdasarkan data yang didapat dari sipsn.menlhk.go.id ,dapat kita lihat bahwa ternyata **Timbulan Sampah** (volume sampah atau berat sampah yang di hasilkan) telah berkurang di setiap tahunnya, hingga pada tahun 2022 mengalami pengurangan **Timbulan Sampah** sebanyak **24.71%**. Kemudian bagaimana dengan pengelolaan dari timbulan sampah tersebut?")

st.header("Penanganan dari Timbulan Sampah")

year = st.selectbox(
    "Pilih tahun yang ingin dilihat",
    [2022,2021,2020,2019]
)

data2 = pd.pivot_table(
    data= capaian[capaian['Tahun']==year],
    index= 'Provinsi',
    aggfunc={
        'Timbulan Sampah Tahunan (ton/tahun)(A)':'sum',
        'Penanganan Sampah Tahunan (ton/tahun)(C)':'sum'
    }
).reset_index()

choice = st.selectbox(
    "Ingin pilih provinsi tertentu?",
    ['Semua Provinsi Saja','Ya']
)
choice

if choice == 'Ya':
    prov = st.multiselect(
    "Pilih Provinsi",
    data2['Provinsi'].values.tolist()
    )
else:
    prov =data2['Provinsi'].values.tolist()


mel_data = data2.melt('Provinsi', var_name='kategori', value_name='jumlah')
mel_datas = mel_data[mel_data['Provinsi'].isin (prov)]

data3 = pd.pivot_table(
    data= mel_datas,
    index= 'kategori',
    aggfunc={
        'jumlah':'sum'
    }
).reset_index()

png = data3.loc[data3['kategori']=='Penanganan Sampah Tahunan (ton/tahun)(C)', 'jumlah'].values[0]
timb = data3.loc[data3['kategori']=='Timbulan Sampah Tahunan (ton/tahun)(A)', 'jumlah'].values[0]
diff = 100*(png)/timb
nopng = timb-png
col1,col2,col3=st.columns(3)

with col1:
    st.metric("Sampah ditangani", value= numerize.numerize(png))
with col2:
    st.metric("Sampah tidak tertangani", value= numerize.numerize(nopng))
with col3:
    st.metric("Persentase Penanganan", value= f'{diff:.2f}%')

trend_bar = alt.Chart(mel_datas).mark_bar().encode(
    alt.X('kategori'),
    alt.Y('jumlah'),
    color='kategori',
    column='Provinsi',
    tooltip=['Provinsi', 'kategori', 'jumlah']
).properties(
    title='Perbandingan Jumlah Sampah dan Penanganan di Tiap Provinsi'
)
st.altair_chart(trend_bar,use_container_width=False)

st.write("Berdasarkan data diatas dapat diketahui bahwa pada tahun 2022 sebanyak 50.30% timbulan sampah tidak tertangani, hal tersebut tentunya perlu ada analisis lebih lanjut tentang ketersediaan TPA serta teknologi yang tersedia di setiap provinsi.")

st.write("Selain itu pada tahun 2022 Provinsi Jawa Tengah menghasilkan timbulan sampah terbanyak, namun penanganan sampahnya kurang dari 50%.")


jenis_sampah = pd.read_csv('https://drive.google.com/uc?export=download&id=1FH_y1c2duwH2X4wr_RofqRirqWfEN4YP')
jenis_sampah.head()
jenis_sampah=jenis_sampah.fillna(0)

st.header("Komposisi Jenis Sampah perTahun")

p= pd.pivot_table(
    data= jenis_sampah[jenis_sampah['Tahun']==year],
    ##data= jenis_sampah,
    index= 'Provinsi',
    aggfunc={
        'Sisa Makanan (%)':'sum',
        'Kayu-Ranting (%)':'sum',
        'Kertas-Karton (%)':'sum',
        'Plastik(%)':'sum',
        'Logam(%)':'sum',
        'Kain(%)':'sum',
        'Karet- Kulit (%)':'sum',
        'Kaca(%)':'sum',
        'Lainnya(%)':'sum'
    }
).reset_index()

total=(p['Kaca(%)'].sum()
  +p['Karet- Kulit (%)'].sum()
  +p['Kertas-Karton (%)'].sum()
  +p['Kain(%)'].sum()
  +p['Kayu-Ranting (%)'].sum()
  +p['Lainnya(%)'].sum()
  +p['Logam(%)'].sum()
  +p['Sisa Makanan (%)'].sum()
  +p['Plastik(%)'].sum()
)

p = p[['Kaca(%)','Kain(%)',	'Karet- Kulit (%)','Kayu-Ranting (%)','Kertas-Karton (%)','Lainnya(%)','Logam(%)',	'Plastik(%)','Sisa Makanan (%)']]/total
p = p[['Kaca(%)','Kain(%)',	'Karet- Kulit (%)','Kayu-Ranting (%)','Kertas-Karton (%)','Lainnya(%)','Logam(%)',	'Plastik(%)','Sisa Makanan (%)']]*100

mel_data2 = p.melt(var_name='kategori', value_name='jumlah')

data4= pd.pivot_table(
    data= mel_data2,
    index= 'kategori',
    aggfunc={
        'jumlah':'sum'
    }
).reset_index()

h=alt.Chart(data4).mark_arc().encode(
    theta="jumlah",
    color="kategori",
    tooltip=['kategori', 'jumlah']
)
st.altair_chart(h,use_container_width=True)

st.write("Berdasarkan data tersebut sampah di Indonesia didominasi oleh **Sampah Sisa Makanan** dan **Sampah Plastik**. Kedua jenis sampah tersebut tentunya memiliki dampak yang berbahaya bagi lingkungan.")

st.write("Berdasarkan informasi dari _ENVIRONMENT INDONESIA CENTER_, dampak dari sampah sisa makanan antara lain:")
st.write("1. Krisis Pangan")
st.write("2. Pemanasan Global")
st.write("3. Limbah Air Lindi")

st.write("Begitupun juga dengan sampah plastik, berdasarkan info dari _Universal Eco_, sampah plastik memiliki dampak berbahaya bagi lingkungan dan manusia. Secara global 90% dari sampah yang mengapung di lautan, 73% diantaranya merupakan sampah plastik. Tentunya hal tersebut akan mencemari biota laut, dan tentunya manusia sebagai konsumen makanan laut akan mendapatkan dampaknya juga.")

pict, teks = st.columns(2)

with pict:
    url2 = 'https://drive.google.com/uc?export=download&id=1VZg8ojH7DxoT8Lp-VP0GmLR5OPwTOQHZ'
    st.image(url2,use_column_width=True)
with teks:
    st.write("Pada SDGs (_Sustainable Development Goals_) nomor 12 yaitu Konsumsi dan Produksi yang Bertanggung Jawab menjadi target negara dan global untuk bisa menyelesaikan masalah tersebut.")
    st.write("Adapun contoh dari hal-hal yang bisa dilakukan dalam kehidupan sehari-hari untuk mewujudkan SDGs nomor 12 ini sebagai berikut:")
    st.write("1. Membeli makan sesuai kebutuhan.")
    st.write("2. Menerapkan 6R (_Refuse_,_Reuse_,_Recycle_,_Root_,_Reduce_ dan _Rethinking_).")
    st.write("3. Menggunakan produk ramah lingkungan sebagai alternatif dari produk plastik.")

st.header("Daftar Pustaka")
st.write("https://www.universaleco.id/blog/detail/dampak-sampah-plastik-terhadap-lingkungan-manusia/95")
st.write("https://environment-indonesia.com/penyebab-food-waste-dan-dampaknya/#:~:text=Sisa%20makanan%20yang%20menumpuk%20dalam,salah%20satu%20pemicu%20pemanasan%20global.")
st.write('https://databoks.katadata.co.id/datapublish/2022/11/12/10-negara-penyumbang-sampah-plastik-terbanyak-ke-laut-ri-peringkat-berapa')
st.write('https://sdgs.bappenas.go.id/tujuan-12/')
st.write('https://sipsn.menlhk.go.id/sipsn/public/data/capaian')