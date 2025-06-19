import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("catboost_model.pkl")

st.title("🚖 Taksi Ücreti Tahmini Uygulaması")

st.markdown("Yolculuk bilgilerini aşağıdan doldur, sistem tahmini fiyatı söylesin!")

# Kullanıcı giriş alanları
passenger_count = st.number_input("Yolcu Sayısı", min_value=1, max_value=6, value=1)
trip_distance = st.number_input("Yolculuk Mesafesi (mil)", min_value=0.0, value=1.5)
PULocationID = st.number_input("Alış Noktası ID", min_value=0, value=130)
DOLocationID = st.number_input("Varış Noktası ID", min_value=0, value=205)
yolculuk_suresi = st.number_input("Yolculuk Süresi (saniye)", min_value=60, value=600)

# Diğer binary değişkenler (1 ya da 0)
jfk_ucreti_mi = st.selectbox("JFK Ücreti Var mı?", [0, 1])
nakit_mi = st.selectbox("Nakit mi?", [0, 1])
pazarlikli_mi = st.selectbox("Pazarlıklı mı?", [0, 1])
nakit_odeme_mi = st.selectbox("Nakit Ödeme mi?", [0, 1])
diger_ucret_mi = st.selectbox("Diğer Ücret Var mı?", [0, 1])

# Giriş verisini oluştur
input_data = pd.DataFrame([{
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
    "yolculuk_suresi": yolculuk_suresi,
    "jfk_ucreti_mi": jfk_ucreti_mi,
    "nakit_mi": nakit_mi,
    "pazarlikli_mi": pazarlikli_mi,
    "nakit_odeme_mi": nakit_odeme_mi,
    "diger_ucret_mi": diger_ucret_mi
}])

# Gerekli olan tüm diğer değişkenleri sıfırla (eksikse model hata verir)
for col in model.feature_names_:
    if col not in input_data.columns:
        input_data[col] = 0

# Sıralama garanti olsun
input_data = input_data[model.feature_names_]

# Tahmin butonu
if st.button("Ücreti Tahmin Et"):
    prediction = model.predict(input_data)[0]
    st.success(f"🚕 Tahmini Ücret: ${prediction:.2f}")
