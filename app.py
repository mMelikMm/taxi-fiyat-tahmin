import streamlit as st
import joblib
import numpy as np
import pandas as pd

# 🔹 Başlık
st.title("🚕 NYC Taksi Ücreti Tahmini (Random Forest Model)")

# 🔹 Modeli Yükle
model = joblib.load("random_forest_model.pkl")

# 🔹 Giriş Verileri
st.header("📥 Yolculuk Bilgilerini Girin")

passenger_count = st.slider("Yolcu Sayısı", 1, 6, 1)
trip_distance = st.number_input("Yolculuk Mesafesi (mil)", min_value=0.1, value=1.5)
PULocationID = st.number_input("Alış Noktası ID", min_value=1, max_value=263, value=10)
DOLocationID = st.number_input("Varış Noktası ID", min_value=1, max_value=263, value=50)
yolculuk_suresi = st.number_input("Yolculuk Süresi (dk)", min_value=1.0, value=10.0)

# Opsiyonel Ekstra Ücretler
jfk_ucreti_mi = st.checkbox("JFK Ücreti Var mı?")
nakit_mi = st.checkbox("Ödeme Türü: Nakit mi?")
nakit_odeme_mi = st.checkbox("Nakit Ödeme Seçildi mi?")
diger_ucret_mi = st.checkbox("Diğer Ücret Var mı?")
pazarlikli_mi = st.checkbox("Pazarlıklı Fiyat mı?")

# 🔹 Tahmin için veri çerçevesi oluştur
input_data = pd.DataFrame({
    "passenger_count": [passenger_count],
    "trip_distance": [trip_distance],
    "PULocationID": [PULocationID],
    "DOLocationID": [DOLocationID],
    "yolculuk_suresi": [yolculuk_suresi],
    "jfk_ucreti_mi": [int(jfk_ucreti_mi)],
    "nakit_mi": [int(nakit_mi)],
    "nakit_odeme_mi": [int(nakit_odeme_mi)],
    "diger_ucret_mi": [int(diger_ucret_mi)],
    "pazarlikli_mi": [int(pazarlikli_mi)]
})

# Geri kalan dummy kolonlar (önemli değilse) 0 olabilir, istersen senin modeline göre ekleriz

# 🔹 Tahmin
if st.button("Ücreti Tahmin Et"):
    tahmin = model.predict(input_data)[0]
    st.success(f"Tahmini Ücret: ${tahmin:.2f}")
