import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("rf_model_light.pkl")

# Başlık
st.title("🚖 NYC Taksi Ücreti Tahmin Uygulaması")
st.markdown("Lütfen aşağıdaki bilgileri girerek tahmini ücreti hesaplayın.")

# Giriş alanları
passenger_count = st.slider("Yolcu Sayısı", 1, 6, 1)
trip_distance = st.number_input("Yolculuk Mesafesi (mil)", min_value=0.1, value=1.0)
yolculuk_suresi = st.number_input("Yolculuk Süresi (dk)", min_value=1.0, value=5.0)

pickup_id = st.number_input("Alış Lokasyon ID", min_value=1, value=130)
dropoff_id = st.number_input("Varış Lokasyon ID", min_value=1, value=249)

jfk_ucreti_mi = st.selectbox("JFK Ücreti Var mı?", ["Hayır", "Evet"])
nakit_odeme_mi = st.selectbox("Nakit Ödeme mi?", ["Hayır", "Evet"])
pazarlikli_mi = st.selectbox("Pazarlıklı mı?", ["Hayır", "Evet"])
diger_ucret_mi = st.selectbox("Diğer Ücret Var mı?", ["Hayır", "Evet"])

# Girdileri dönüştür
input_dict = {
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "yolculuk_suresi": yolculuk_suresi,
    "PULocationID": pickup_id,
    "DOLocationID": dropoff_id,
    "jfk_ucreti_mi": 1 if jfk_ucreti_mi == "Evet" else 0,
    "nakit_odeme_mi": 1 if nakit_odeme_mi == "Evet" else 0,
    "pazarlikli_mi": 1 if pazarlikli_mi == "Evet" else 0,
    "diger_ucret_mi": 1 if diger_ucret_mi == "Evet" else 0
}

# Veri çerçevesi oluştur
input_df = pd.DataFrame([input_dict])

# Tahmin
if st.button("Tahmini Ücreti Hesapla"):
    prediction = model.predict(input_df)[0]
    st.success(f"🚕 Tahmini Ücret: ${prediction:.2f}")
