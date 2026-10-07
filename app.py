import streamlit as st
import pandas as pd
import json
import os

# App Title & Configuration
st.set_page_config(page_title="Student Result Management System", layout="centered")

st.title("🎓 Student Result Management System")
st.write("Welcome! Enter student details below to calculate WAEC grades and save records.")

# File for local persistence
DATA_FILE = "student_results.json"

# Function to calculate WAEC Grade
def calculate_waec_grade(score):
    if score >= 75:
        return "A1 (Excellent)"
    elif score >= 70:
        return "B2 (Very Good)"
    elif score >= 65:
        return "B3 (Good)"
    elif score >= 50:
        return "C6 (Credit)"
    elif score >= 40:
        return "E8 (Pass)"
    else:
        return "F9 (Fail)"

# Load saved records
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        st.session_state.records = json.load(f)
elif "records" not in st.session_state:
    st.session_state.records = []

# --- INPUT FORM ---
st.header("📌 Add Student Record")

with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        math = st.number_input("Mathematics", min_value=0.0, max_value=100.0, step=1.0)
    with col2:
        eng = st.number_input("English", min_value=0.0, max_value=100.0, step=1.0)
    with col3:
        phy = st.number_input("Physics", min_value=0.0, max_value=100.0, step=1.0)
        
    submitted = st.form_submit_button("Save Student Record")

if submitted:
    if name.strip() == "":
        st.error("Please enter a valid student name!")
    else:
        avg = (math + eng + phy) / 3.0
        grade = calculate_waec_grade(avg)
        
        new_entry = {
            "Name": name,
            "Mathematics": math,
            "English": eng,
            "Physics": phy,
            "Average (%)": round(avg, 2),
            "Overall Grade": grade
        }
        
        st.session_state.records.append(new_entry)
        
        # Save to local file
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.records, f, indent=4)
            
        st.success(f"Record for {name} saved successfully!")

# --- DISPLAY RECORDS ---
st.divider()
st.header("📊 Saved Student Records")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df, use_container_width=True)
    
    if st.button("Clear All Records"):
        st.session_state.records = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.rerun()
else:
    st.info("No records stored yet. Add a student above!")
  
