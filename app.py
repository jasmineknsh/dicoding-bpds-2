import streamlit as st
import pandas as pd
import joblib

# --- Load model dan encoder ---
model = joblib.load("model/rf_model2.pkl")
encoder = joblib.load("model/onehot_encoder2.pkl")

# Fitur input
important_categorical = ['Application_mode', 'Course', 'Gender', 'Previous_qualification']
important_numerical = [
    'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade',
    'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade',
    'Tuition_fees_up_to_date', 'Scholarship_holder', 'Age_at_enrollment',
    'Debtor'
]

st.title("🎓 Prediksi Dropout Mahasiswa")
st.markdown("© 2025 Jasmine Kinasih")

st.subheader("📝 Masukkan Data Mahasiswa")

# === Fungsi untuk encoding input ===
def encode_input(df, encoder, cat_cols, num_cols):
    X_cat = encoder.transform(df[cat_cols])
    cat_names = encoder.get_feature_names_out(cat_cols)
    X_num = df[num_cols].reset_index(drop=True)
    X_ready = pd.concat([X_num, pd.DataFrame(X_cat, columns=cat_names, index=X_num.index)], axis=1)
    return X_ready

# Form Input
with st.form("form_input"):
    # --- Input Numerikal
    st.subheader("📊 Data Performa Akademik & Finansial")
    sem2_approved = st.number_input("2nd Semester - Mata kuliah lulus", min_value=0, step=1)
    sem2_grade = st.number_input("2nd Semester - Nilai rata-rata", min_value=0.0)
    sem1_approved = st.number_input("1st Semester - Mata kuliah lulus", min_value=0, step=1)
    sem1_grade = st.number_input("1st Semester - Nilai rata-rata", min_value=0.0)

    tuition_up_to_date = st.radio("Apakah pembayaran UKT/Lunas?", ["Ya", "Tidak"])
    tuition_up_to_date = 1 if tuition_up_to_date == "Ya" else 0

    scholarship = st.radio("Penerima Beasiswa?", ["Ya", "Tidak"])
    scholarship = 1 if scholarship == "Ya" else 0

    # --- Input Kategorikal
    st.subheader("🧾 Data Demografi dan Faktor Lainnya")
    age = st.number_input("Usia saat masuk kuliah", min_value=15)
    
    debtor = st.radio("Apakah memiliki utang pendidikan?", ["Ya", "Tidak"])
    debtor = 1 if debtor == "Ya" else 0

    app_mode = st.selectbox("Metode Pendaftaran (Application Mode)", [
        "1st Phase - General Contingent",
        "1st Phase - Special Contingent (Azores Island)",
        "1st Phase - Special Contingent (Madeira Island)",
        "2nd Phase - General Contingent",
        "3rd Phase - General Contingent",
        "Ordinance No. 612/93",
        "Ordinance No. 854-B/99",
        "International Student (Bachelor)",
        "Over 23 Years Old",
        "Transfer",
        "Change of Course",
        "Holders of Other Higher Courses",
        "Short Cycle Diploma Holders",
        "Technological Specialization Diploma Holders",
        "Change of Institution/Course",
        "Change of Institution/Course (International)"
    ], help="Metode aplikasi yang dipakai mahasiswa")

    course = st.selectbox("Program Studi (Course)", [
        "Biofuel Production Technologies",
        "Animation and Multimedia Design",
        "Social Service (Evening Attendance)",
        "Agronomy",
        "Communication Design",
        "Veterinary Nursing",
        "Informatics Engineering",
        "Equinculture",
        "Management",
        "Social Service",
        "Tourism",
        "Nursing",
        "Oral Hygiene",
        "Advertising and Marketing Management",
        "Journalism and Communication",
        "Basic Education",
        "Management (Evening Attendance)"
    ], help="Program studi yang diikuti")

    gender = st.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    gender = 0 if gender == "Perempuan" else 1

    prev_qual = st.selectbox("Kualifikasi Pendidikan Sebelumnya", [
        "1 - Sekolah Menengah Atas",
        "2 - Sekolah Teknik",
        "3 - Sertifikat Vokasi",
        "4 - Diploma",
        "5 - Sarjana",
        "6 - Lainnya"
    ])
    prev_qual = int(prev_qual.split(" - ")[0])

    submitted = st.form_submit_button("Prediksi")

    
    
# Proses prediksi
if submitted:
    # Siapkan data input
    data_input = pd.DataFrame([{
        'Application_mode': app_mode,
        'Course': course,
        'Gender': gender,  # Sudah dalam bentuk 0 atau 1 dari radio
        'Previous_qualification': prev_qual,  # Sudah dalam bentuk int
        'Curricular_units_2nd_sem_approved': sem2_approved,
        'Curricular_units_2nd_sem_grade': sem2_grade,
        'Curricular_units_1st_sem_approved': sem1_approved,
        'Curricular_units_1st_sem_grade': sem1_grade,
        'Tuition_fees_up_to_date': tuition_up_to_date,
        'Scholarship_holder': scholarship,
        'Age_at_enrollment': age,
        'Debtor': debtor
    }])

    # Encoding fitur kategorikal
    X_cat = encoder.transform(data_input[important_categorical])
    cat_cols = encoder.get_feature_names_out(important_categorical)
    df_cat = pd.DataFrame(X_cat, columns=cat_cols)

    # Ambil fitur numerikal
    X_num = data_input[important_numerical].reset_index(drop=True)

    # Gabungkan keduanya
    final_input = pd.concat([X_num, df_cat], axis=1)

    # Prediksi
    prediction = model.predict(final_input)[0]
    proba = model.predict_proba(final_input)[0]

    # Tampilkan hasil
    st.subheader("📈 Hasil Prediksi")
    if prediction == 0:
        st.error(f"⚠️ Mahasiswa kemungkinan besar **Dropout**. Probabilitas: {proba[0]:.2%}")
    else:
        st.success(f"✅ Mahasiswa kemungkinan **Bertahan / Lulus**. Probabilitas: {proba[1]:.2%}")
