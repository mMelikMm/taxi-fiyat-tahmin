import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("rf_model_light.pkl")

# Başlık
st.title("🚖 NYC Taksi Ücreti Tahmin Uygulaması")
st.markdown("Lütfen aşağıdaki bilgileri girin:")

# Girişler
passenger_count = st.slider("Yolcu Sayısı", 1, 6, 1)
trip_distance = st.number_input("Yolculuk Mesafesi (mil)", min_value=0.1, value=1.0)
yolculuk_suresi = st.number_input("Yolculuk Süresi (dk)", min_value=1.0, value=5.0)
PULocationID = st.number_input("Alış Lokasyon ID", min_value=1, value=130)
DOLocationID = st.number_input("Varış Lokasyon ID", min_value=1, value=249)
pazarlikli_mi = st.selectbox("Pazarlıklı mı?", ["Hayır", "Evet"])
jfk_ucreti_mi = st.selectbox("JFK Ekstra Ücreti Var mı?", ["Hayır", "Evet"])
diger_ucret_mi = st.selectbox("Diğer Ekstra Ücret Var mı?", ["Hayır", "Evet"])
nakit_odeme_mi = st.selectbox("Nakit Ödeme mi?", ["Hayır", "Evet"])

# Giriş verisini doğru sırayla alalım
columns_order = [
    'passenger_count',
    'trip_distance',
    'PULocationID',
    'DOLocationID',
    'yolculuk_suresi',
    'pazarlikli_mi',
    'jfk_ucreti_mi',
    'diger_ucret_mi',
    'nakit_odeme_mi'
]

input_data = pd.DataFrame([[
    passenger_count,
    trip_distance,
    PULocationID,
    DOLocationID,
    yolculuk_suresi,
    1 if pazarlikli_mi == "Evet" else 0,
    1 if jfk_ucreti_mi == "Evet" else 0,
    1 if diger_ucret_mi == "Evet" else 0,
    1 if nakit_odeme_mi == "Evet" else 0
]], columns=columns_order)

# Tahmin
if st.button("Tahmini Ücreti Hesapla"):
    prediction = model.predict(input_data)[0]
    st.success(f"Tahmini Ücret: ${prediction:.2f}")
