
  
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Result Management System", page_icon="🎓", layout="wide")

# --- INITIALIZE SESSION STATES ---
if "student_records" not in st.session_state:
    st.session_state.student_records = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

subjects = [
    "Mathematics", "English Language", "Physics", "Chemistry", "Biology",
    "Civic Education", "Digital Technology", "Economics", "Geography"
]

# --- SIDEBAR: WAEC PAST QUESTIONS PRACTICE ---
st.sidebar.title("📚 WAEC Past Questions")
st.sidebar.write("Practice real WAEC multiple-choice questions below!")

# Sample WAEC Past Questions Bank
waec_questions = {
    "Mathematics": {
        "question": "Solve for x: 2x + 5 = 15",
        "options": ["x = 3", "x = 5", "x = 10", "x = 7"],
        "answer": "x = 5"
    },
    "English Language": {
        "question": "Choose the word nearest in meaning to 'ABUNDANT':",
        "options": ["Scarce", "Plentiful", "Small", "Empty"],
        "answer": "Plentiful"
    },
    "Physics": {
        "question": "What is the SI unit of force?",
        "options": ["Joule", "Watt", "Newton", "Pascal"],
        "answer": "Newton"
    },
    "Chemistry": {
        "question": "What is the chemical symbol for Gold?",
        "options": ["Ag", "Au", "Fe", "Pb"],
        "answer": "Au"
    },
    "Biology": {
        "question": "Which organelle is known as the powerhouse of the cell?",
        "options": ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"],
        "answer": "Mitochondria"
    },
    "Civic Education": {
        "question": "Which of the following is a key characteristic of democracy?",
        "options": ["Rule of Law", "Dictatorship", "Monarchy", "Military Rule"],
        "answer": "Rule of Law"
    },
    "Digital Technology": {
        "question": "What does CPU stand for?",
        "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Control Program Unit"],
        "answer": "Central Processing Unit"
    },
    "Economics": {
        "question": "What happens to demand when price increases (holding other factors constant)?",
        "options": ["Increases", "Decreases", "Remains Constant", "Fluctuate"],
        "answer": "Decreases"
    },
    "Geography": {
        "question": "Which layer of the atmosphere contains the ozone layer?",
        "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"],
        "answer": "Stratosphere"
    }
}

selected_sub = st.sidebar.selectbox("Select Subject to Practice:", subjects)

q_data = waec_questions[selected_sub]
st.sidebar.markdown(f"**Question:** {q_data['question']}")
user_choice = st.sidebar.radio("Choose an option:", q_data["options"], key=f"q_{selected_sub}")

if st.sidebar.button("Submit Answer"):
    if user_choice == q_data["answer"]:
        st.sidebar.success("🎉 Correct Answer!")
        st.session_state.quiz_score += 1
    else:
        st.sidebar.error(f"❌ Incorrect. Correct answer: {q_data['answer']}")

st.sidebar.info(f"**Practice Session Score:** {st.session_state.quiz_score} correct")


# --- MAIN APP: RESULT MANAGEMENT ---
st.title("🎓 Student Result Management System")
st.write("Welcome! Enter student assessment scores below to compute totals, averages, and class rankings.")

st.header("📌 Add Student Record")

with st.form("student_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    
    st.markdown("### 📝 Enter Subject Scores")
    st.caption("Max scores — Classwork: 10 | Homework: 10 | Test/CA: 20 | Exam: 60 (Total: 100 per subject)")
    
    subject_scores = {}
    
    for sub in subjects:
        st.subheader(f"📚 {sub}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cw = st.number_input(f"{sub} - Classwork (10)", min_value=0.0, max_value=10.0, step=1.0, key=f"{sub}_cw")
        with col2:
            hw = st.number_input(f"{sub} - Homework (10)", min_value=0.0, max_value=10.0, step=1.0, key=f"{sub}_hw")
        with col3:
            ca = st.number_input(f"{sub} - Test / CA (20)", min_value=0.0, max_value=20.0, step=1.0, key=f"{sub}_ca")
        with col4:
            exam = st.number_input(f"{sub} - Exam (60)", min_value=0.0, max_value=60.0, step=1.0, key=f"{sub}_exam")
            
        sub_total = cw + hw + ca + exam
        subject_scores[sub] = sub_total

    submitted = st.form_submit_button("Save Student Record")

if submitted:
    if not name.strip():
        st.error("Please enter the student's full name.")
    else:
        grand_total = sum(subject_scores.values())
        average = grand_total / len(subjects)
        
        record = {"Name": name.strip(), "Total Score": grand_total, "Average (%)": round(average, 2)}
        record.update(subject_scores)
        
        st.session_state.student_records.append(record)
        st.success(f"Record saved for **{name}**!")

# --- DISPLAY CLASS RECORDS & POSITIONS ---
if st.session_state.student_records:
    st.markdown("---")
    st.header("📊 Class Results & Position Summary")
    
    df = pd.DataFrame(st.session_state.student_records)
    df["Position"] = df["Total Score"].rank(ascending=False, method="min").astype(int)
    
    def get_ordinal(n):
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    df["Position"] = df["Position"].apply(get_ordinal)
    
    cols = ["Position", "Name", "Total Score", "Average (%)"] + subjects
    df = df[cols].sort_values("Total Score", ascending=False)
    
    st.dataframe(df, use_container_width=True)
