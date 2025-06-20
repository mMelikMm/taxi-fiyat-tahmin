import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Modeli yükle
model = joblib.load("catboost_model.pkl")

# Başlık ve açıklama
st.set_page_config(page_title="Taksi Ücreti Tahmini", page_icon="🚖")
st.title("🚖 Taksi Ücreti Tahmini Uygulaması")
st.markdown("New York City içindeki bir yolculuk için **tahmini ücret** öğrenmek ister misin? 👇")

# Yan panel - görsel koyabilirsin
with st.sidebar:
    st.image("https://i.imgur.com/NKX5oIY.png", caption="NYC Taxi", use_column_width=True)
    st.markdown("Bu uygulama bir Machine Learning projesidir.")
    st.markdown("**Model:** CatBoost Regressor")
    st.markdown("Veri: NYC Yellow Taxi")

# Giriş alanları
st.subheader("🚕 Yolculuk Bilgilerini Gir")

passenger_count = st.slider("Yolcu Sayısı", 1, 6, 1)
trip_distance = st.number_input("Yolculuk Mesafesi (mil)", min_value=0.1, value=1.5, step=0.1)
PULocationID = st.number_input("Alış Noktası ID", min_value=0, value=130)
DOLocationID = st.number_input("Varış Noktası ID", min_value=0, value=205)
trip_duration_min = st.slider("Yolculuk Süresi (dakika)", 1, 120, 10)
trip_duration_sec = trip_duration_min * 60  # modele uygun olması için

# Diğer binary değişkenler
col1, col2, col3 = st.columns(3)
with col1:
    jfk_ucreti_mi = st.radio("JFK Ücreti Var mı?", [0, 1])
with col2:
    nakit_mi = st.radio("Nakit mi?", [0, 1])
with col3:
    pazarlikli_mi = st.radio("Pazarlıklı mı?", [0, 1])

col4, col5 = st.columns(2)
with col4:
    nakit_odeme_mi = st.radio("Nakit Ödeme mi?", [0, 1])
with col5:
    diger_ucret_mi = st.radio("Diğer Ücret Var mı?", [0, 1])

# Giriş verisi
input_data = pd.DataFrame([{
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
    "yolculuk_suresi": trip_duration_sec,
    "jfk_ucreti_mi": jfk_ucreti_mi,
    "nakit_mi": nakit_mi,
    "pazarlikli_mi": pazarlikli_mi,
    "nakit_odeme_mi": nakit_odeme_mi,
    "diger_ucret_mi": diger_ucret_mi
}])

# Modelin beklediği tüm sütunları kontrol et
for col in model.feature_names_:
    if col not in input_data.columns:
        input_data[col] = 0

# Sıralama garanti
input_data = input_data[model.feature_names_]

# Tahmin
if st.button("🎯 Tahmini Ücreti Hesapla"):
    prediction = model.predict(input_data)[0]
    st.success(f"🚕 Tahmini Taksi Ücreti: **${prediction:.2f}**")
