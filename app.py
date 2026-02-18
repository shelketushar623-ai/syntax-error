import streamlit as st
import pandas as pd
import os

# ===============================
# Page Config (ONLY ONCEpy
# ===============================
st.set_page_config(page_title="Telemedicine Queue", layout="wide", page_icon="logo.png")

# Show Logo (will work only if logo.png.png is a valid image)
col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png.png", width=100)

with col2:
    st.markdown("<h1 style='margin-top: 20px;'>Telemed</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top: -10px; color: gray;'>Doctor Dashboard</h4>", unsafe_allow_html=True)

# ===============================
# Setup & Persistence Config
# ===============================
DB_FILE = "patient_data.csv"
TIME_PER_PATIENT_MIN = 10  # assuming 10 minutes per patient

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Name", "Age", "Severity", "Emergency", "Priority"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# ===============================
# Initialize Session State
# ===============================
if "df" not in st.session_state:
    st.session_state.df = load_data()

# ===============================
# Header Metrics
# ===============================
total_patients = len(st.session_state.df)
st.metric(label="👥 Total Patients in Queue", value=total_patients)

# ===============================
# Sidebar: Add Patient
# ===============================
with st.sidebar:
    st.header("🧾 Register Patient")
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", 0, 120, 30)
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        emergency = st.selectbox("Emergency Case?", ["No", "Yes"])
        submit_btn = st.form_submit_button("Add to Queue")

        if submit_btn:
            if name.strip():
                # Priority Logic (Rule-based triage)
                score = {"High": 3, "Medium": 2, "Low": 1}[severity]
                if age > 60:
                    score += 1
                if emergency == "Yes":
                    score += 2

                new_entry = pd.DataFrame(
                    [[name, age, severity, emergency, score]],
                    columns=st.session_state.df.columns
                )

                st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)
                save_data(st.session_state.df)
                st.success(f"Registered: {name}")
            else:
                st.error("Please enter a name!")

# ===============================
# Main: Display Queue
# ===============================
st.subheader("📋 Priority Triage List")

if not st.session_state.df.empty:
    # Sort by Priority (High to Low)
    display_df = st.session_state.df.sort_values(by="Priority", ascending=False).reset_index(drop=True)

    # Add Estimated Waiting Time column
    display_df["Estimated Wait (min)"] = display_df.index * TIME_PER_PATIENT_MIN

    # Highlight Next Patient
    next_patient = display_df.iloc[0]
    st.success(
        f"🟢 Next to Consult: {next_patient['Name']} "
        f"(Priority: {int(next_patient['Priority'])}, "
        f"Estimated Wait: {int(next_patient['Estimated Wait (min)'])} min)"
    )

    # Show table
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Action Button
    if st.button("✅ Attend Next Patient"):
        top_name = display_df.iloc[0]["Name"]
        st.session_state.df = st.session_state.df[st.session_state.df["Name"] != top_name]
        save_data(st.session_state.df)
        st.rerun()
else:
    st.info("The queue is currently empty.")
