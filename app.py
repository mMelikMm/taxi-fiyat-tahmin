import streamlit as st
import numpy as np
import joblib
from catboost import CatBoostRegressor
import joblib


# Modeli yükle
model = joblib.load("catboost_model.pkl")

st.title("🚕 Taksi Ücreti Tahmin Uygulaması")

st.markdown("📍 Aşağıdaki bilgileri doldurarak tahmini taksi ücretini hesaplayabilirsin.")

# Kullanıcıdan veri al
passenger_count = st.slider("Yolcu Sayısı", 1, 6, step=1)
trip_distance = st.number_input("Mesafe (mil)", min_value=0.1, step=0.1)
PULocationID = st.number_input("Alınan Lokasyon ID", min_value=1, step=1)
DOLocationID = st.number_input("İnilen Lokasyon ID", min_value=1, step=1)
yolculuk_suresi = st.number_input("Yolculuk Süresi (dakika)", min_value=1.0, step=1.0)

yogun_saat_mi = st.checkbox("Yoğun Saat mi?")
haftaici_mi = st.checkbox("Haftaiçi mi?")
gunduz_mü = st.checkbox("Gündüz mü?")
nakit_mi = st.checkbox("Nakit mi?")
kisa_yolculuk_mu = st.checkbox("Kısa Yolculuk mu?")
store_and_fwd_flag_Y = st.checkbox("Store & Fwd Flag (Y)")
jfk_ucreti_mi = st.checkbox("JFK Ek Ücreti Var mı?")
newark_ucreti_mi = st.checkbox("Newark Ek Ücreti Var mı?")
nassau_westchester_mi = st.checkbox("Nassau/Westchester Ücreti Var mı?")
pazarlikli_mi = st.checkbox("Pazarlıklı mı?")
diger_ucret_mi = st.checkbox("Diğer Ücret Var mı?")
VendorID_2 = st.checkbox("VendorID 2 mi?")
nakit_odeme_mi = st.checkbox("Nakit Ödeme mi?")
ucretsiz_mi = st.checkbox("Ücretsiz Yolculuk mu?")

# Tahmin butonu
if st.button("🚖 Tahmini Ücreti Hesapla"):
    input_data = np.array([[
        passenger_count, trip_distance, PULocationID, DOLocationID,
        yolculuk_suresi, int(yogun_saat_mi), int(haftaici_mi),
        int(gunduz_mü), int(nakit_mi), int(kisa_yolculuk_mu),
        int(store_and_fwd_flag_Y), int(jfk_ucreti_mi), int(newark_ucreti_mi),
        int(nassau_westchester_mi), int(pazarlikli_mi), int(diger_ucret_mi),
        int(VendorID_2), int(nakit_odeme_mi), int(ucretsiz_mi)
    ]])

    tahmin = model.predict(input_data)[0]
    st.success(f"💵 Tahmini Ücret: {tahmin:.2f} $")
