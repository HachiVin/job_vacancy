import streamlit as st
import json
import os
from pathlib import Path

# ==============================
# STEP 1 — Load JSON Data
# ==============================
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

vacancy_data = load_json("job_vacancy.json")
output_data = load_json("output.json")

# ==============================
# STEP 2 — Setup Streamlit Page
# ==============================
st.set_page_config(page_title="Job Application AI", layout="wide")
st.title("Job Vacancy")
st.markdown("Unggah CV kamu dan pilih lowongan yang ingin dilamar.")

# ==============================
# STEP 3 — Pilih Job Vacancy
# ==============================
jobs = [vacancy_data["data"]["name"]]  # bisa diubah ke list banyak job nanti
selected_job = st.selectbox("🧾 Pilih Lowongan Pekerjaan:", jobs)

if selected_job:
    job = vacancy_data["data"]

    st.subheader(f"📋 Detail Lowongan — {job['name']}")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Tipe:** {job['type']}")
        st.markdown(f"**Lokasi:** {job['city']['name']}, {job['province']['name']}")
        st.markdown(f"**Pendidikan Minimal:** {job['minEducation'].upper()}")
        st.markdown(f"**Pengalaman:** {job['minYearExperience']}")
        st.markdown(f"**Keahlian:** {', '.join(job['skills'])}")
    with col2:
        st.markdown(f"**Perusahaan:** {job['company']['name']}")
        st.markdown(f"**Range Gaji:** Rp{job['minSalary']:,} - Rp{job['maxSalary']:,}")
        st.markdown(f"**Dibuat pada:** {job['createdAt']}")

    with st.expander("📄 Deskripsi Pekerjaan"):
        st.markdown(job["description"])

# ==============================
# STEP 4 — Upload CV File
# ==============================
st.divider()
st.subheader("📤 Unggah CV Kamu")

uploaded_cv = st.file_uploader("Pilih file CV (PDF saja)", type=["pdf"])

if uploaded_cv:
    # Simpan CV ke folder uploads/
    uploads_path = Path("uploads")
    uploads_path.mkdir(exist_ok=True)
    save_path = uploads_path / uploaded_cv.name

    with open(save_path, "wb") as f:
        f.write(uploaded_cv.getbuffer())

    st.success(f"✅ CV berhasil diunggah: `{uploaded_cv.name}`")
    st.info("File tersimpan di folder `uploads/`")

    # Tombol Apply
    if st.button("📨 Apply Job Sekarang"):
        st.success(f"Lamaran berhasil dikirim untuk posisi **{selected_job}**!")
        st.toast("CV berhasil dikirim!", icon="📬")

        # Simulasi hasil analisis AI (dari output.json)
        st.divider()
        st.subheader("🤖 Hasil Analisis CV oleh AI")

        st.markdown(f"**AI Recommendation for HR:** {output_data['ai_recommendation_for_hr']}")
        st.markdown(f"**AI Recommendation for Candidate:** {output_data['ai_recommendation_for_candidate']}")

        st.markdown("### 🧩 Gap Analysis")
        st.write(output_data["gap_analysis"])

        # SWOT
        swot = output_data["swot_analysis"]
        st.markdown("### 💪 Strengths")
        st.markdown("\n".join([f"- {s}" for s in swot["strengths"]]))

        st.markdown("### ⚠️ Weaknesses")
        st.markdown("\n".join([f"- {s}" for s in swot["weaknesses"]]))

        st.markdown("### 🌱 Opportunities")
        st.markdown("\n".join([f"- {s}" for s in swot["opportunities"]]))

        st.markdown("### 🚧 Threats")
        st.markdown("\n".join([f"- {s}" for s in swot["threats"]]))

