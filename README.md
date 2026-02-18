# syntax-error
AI-assisted telemedicine queue optimization system that prioritizes patients using rule-based triage, shows next patient, estimates waiting time, and provides a doctor dashboard built with Python and Streamlit.
# 🩺 Telemed – AI-Assisted Telemedicine Queue Optimization

This project is a **hackathon prototype** for an AI-assisted telemedicine queue optimization system.  
It helps doctors **prioritize patients** instead of using first-come-first-serve by applying a **rule-based triage and priority scoring system**.

---

## 🚀 Features

- 🧑‍⚕️ Doctor Dashboard
- 📋 Priority-based triage list
- 🟢 Highlights **Next Patient to Consult**
- ⏱️ Shows **Estimated Waiting Time**
- 👥 Displays **Total Patients in Queue**
- 💾 Data persistence using CSV (does not reset on restart)
- ✅ One-click **Attend Next Patient** action
- 🧾 Sidebar form to register patients

---

## 🧠 How the “AI” Works

The system uses a **rule-based priority scoring algorithm** based on:
- Severity (Low / Medium / High)
- Age (Senior citizens get higher priority)
- Emergency status (Emergency cases get extra priority)

Each patient gets a **priority score**, and the queue is sorted from **highest to lowest priority**.  
This makes the system **transparent and explainable**, which is important in healthcare decision support systems.

---

## 🛠️ Tech Stack

- Python
- Streamlit (Web UI)
- Pandas (Data handling)
- CSV (Local storage)
- GitHub (Version control)

---

## ▶️ How to Run

1. Install dependencies:
```bash
pip install streamlit pandas
