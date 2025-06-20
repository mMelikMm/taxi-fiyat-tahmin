import streamlit as st
import pandas as pd
import joblib

# Sayfa ayarları
st.set_page_config(page_title="Taksi Ücreti Tahmini", page_icon="🚖", layout="centered")

# Başlık
st.title("🚖 NYC Taksi Ücreti Tahmini Uygulaması")
st.markdown("Gerçek veriye dayalı, **akıllı fiyat tahmin** sistemiyle tanışın! 💰")

st.divider()

# 🔻 Giriş alanları (iki sütunlu görünüm)
col1, col2 = st.columns(2)

with col1:
    passenger_count = st.number_input("👥 Yolcu Sayısı", min_value=1, max_value=6, value=1)
    trip_distance = st.number_input("📏 Mesafe (mil)", min_value=0.0, value=1.5)
    PULocationID = st.number_input("📍 Alış Noktası ID", min_value=0, value=130)
    yolculuk_suresi = st.number_input("⏱️ Süre (saniye)", min_value=60, value=600)
    jfk_ucreti_mi = st.radio("🛫 JFK Ücreti Var mı?", [0, 1], horizontal=True)

with col2:
    DOLocationID = st.number_input("🎯 Varış Noktası ID", min_value=0, value=205)
    nakit_mi = st.radio("💵 Nakit mi?", [0, 1], horizontal=True)
    pazarlikli_mi = st.radio("🤝 Pazarlıklı mı?", [0, 1], horizontal=True)
    
    diger_ucret_mi = st.radio("➕ Diğer Ücret Var mı?", [0, 1], horizontal=True)

st.divider()

# Modeli yükle
model = joblib.load("catboost_model.pkl")

# Giriş verisi
input_data = pd.DataFrame([{
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
    "yolculuk_suresi": yolculuk_suresi,
    "jfk_ucreti_mi": jfk_ucreti_mi,
    "nakit_mi": nakit_mi,
    "pazarlikli_mi": pazarlikli_mi,
    "diger_ucret_mi": diger_ucret_mi
}])

# Gerekirse eksik kolonları sıfırla
for col in model.feature_names_:
    if col not in input_data.columns:
        input_data[col] = 0

# Sütun sıralaması garanti olsun
input_data = input_data[model.feature_names_]

# Tahmin
if st.button("🚕 Tahmini Ücreti Hesapla"):
    prediction = model.predict(input_data)[0]
    st.success(f"💰 **Tahmini Ücret: ${prediction:.2f}**")

    st.caption("📊 Bu tahmin, CatBoost modeli ile gerçek NYC taksi verilerine dayanarak yapılmıştır.")
