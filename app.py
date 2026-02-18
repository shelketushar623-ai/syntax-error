import streamlit as st
import pandas as pd
import os

# ===============================
# Page Config (ONLY ONCE)
# ===============================
st.set_page_config(page_title="Telemedicine Queue", layout="wide", page_icon="new.png.png")

# Show Logo + Title
st.image("new.png.png", width=200)
st.title(" Telemed – Doctor Dashboard")

# ===============================
# Setup & Persistence
# ===============================
DB_FILE = "patient_data.csv"
TIME_PER_PATIENT_MIN = 10  # assume 10 minutes per patient

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

if "doctor_available" not in st.session_state:
    st.session_state.doctor_available = True

# ===============================
# Header Metrics
# ===============================
total_patients = len(st.session_state.df)
st.metric(label="👥 Total Patients in Queue", value=total_patients)

# ===============================
# Sidebar Controls
# ===============================
with st.sidebar:
    st.header("👨‍⚕️ Doctor Status")
    doctor_status = st.toggle("Doctor Available", value=st.session_state.doctor_available)
    st.session_state.doctor_available = doctor_status

    if not st.session_state.doctor_available:
        st.warning("Doctor is currently unavailable. Queue will be maintained and emergencies are flagged.")

    st.divider()

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

    # Mark Emergency for visibility
    display_df["Emergency Flag"] = display_df["Emergency"].apply(lambda x: "🚨 EMERGENCY" if x == "Yes" else "")

    # Show table
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    top_patient = display_df.iloc[0]

    if st.session_state.doctor_available:
        # Doctor is available → show next patient
        st.success(
            f"🟢 Next to Consult: {top_patient['Name']} "
            f"(Priority: {int(top_patient['Priority'])}, "
            f"Estimated Wait: {int(top_patient['Estimated Wait (min)'])} min)"
        )

        if st.button("✅ Attend Next Patient"):
            top_name = top_patient["Name"]
            st.session_state.df = st.session_state.df[st.session_state.df["Name"] != top_name]
            save_data(st.session_state.df)
            st.rerun()
    else:
        # Doctor not available → hold queue, flag emergencies
        if top_patient["Emergency"] == "Yes":
            st.error("🚨 Emergency case at top of queue! Doctor unavailable. Please redirect or wait.")
        else:
            st.warning("Doctor unavailable. Queue is on hold. Waiting times will continue to update.")
else:
    st.info("The queue is currently empty.")

