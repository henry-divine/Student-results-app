
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Result & WAEC Practice System", page_icon="🎓", layout="wide")

# --- INITIALIZE SESSION STATE ---
if "student_records" not in st.session_state:
    st.session_state.student_records = []
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

subjects = [
    "Mathematics", "English Language", "Physics", "Chemistry", "Biology",
    "Civic Education", "Digital Technology", "Economics", "Geography"
]

# Comprehensive WAEC Past Questions Bank (Multiple questions per subject)
waec_questions = {
    "Mathematics": [
        {"question": "Solve for x: 2x + 5 = 15", "options": ["x = 3", "x = 5", "x = 10", "x = 7"], "answer": "x = 5"},
        {"question": "Evaluate 0.075 x 10^4", "options": ["7.5", "75", "750", "7500"], "answer": "750"},
        {"question": "Find the simple interest on N5,000 for 2 years at 5% per annum.", "options": ["N250", "N500", "N750", "N1,000"], "answer": "N500"},
        {"question": "Factorize completely: 3x^2 - 12", "options": ["3(x-2)(x+2)", "3(x-4)(x+4)", "(3x-2)(x+2)", "3(x-2)^2"], "answer": "3(x-2)(x+2)"},
        {"question": "If the interior angle of a regular polygon is 140°, find the number of sides.", "options": ["6", "8", "9", "10"], "answer": "9"}
    ],
    "English Language": [
        {"question": "Choose the word nearest in meaning to 'ABUNDANT':", "options": ["Scarce", "Plentiful", "Small", "Empty"], "answer": "Plentiful"},
        {"question": "Choose the word opposite in meaning to 'ANCIENT':", "options": ["Old", "Modern", "Antique", "Primitive"], "answer": "Modern"},
        {"question": "Choose the correct option to fill the gap: Neither the teacher nor the students ___ present.", "options": ["was", "were", "is", "has been"], "answer": "were"},
        {"question": "What figure of speech is used in: 'The wind whispered through the dark trees'?", "options": ["Simile", "Metaphor", "Personification", "Hyperbole"], "answer": "Personification"}
    ],
    "Physics": [
        {"question": "What is the SI unit of force?", "options": ["Joule", "Watt", "Newton", "Pascal"], "answer": "Newton"},
        {"question": "Which of the following is a vector quantity?", "options": ["Speed", "Mass", "Velocity", "Distance"], "answer": "Velocity"},
        {"question": "The time taken for a pendulum to complete one full oscillation is called:", "options": ["Frequency", "Period", "Amplitude", "Wavelength"], "answer": "Period"},
        {"question": "What device is used to measure relative humidity?", "options": ["Hydrometer", "Barometer", "Hygrometer", "Manometer"], "answer": "Hygrometer"}
    ],
    "Chemistry": [
        {"question": "What is the chemical symbol for Gold?", "options": ["Ag", "Au", "Fe", "Pb"], "answer": "Au"},
        {"question": "What is the pH of a neutral solution at 25°C?", "options": ["0", "7", "14", "5"], "answer": "7"},
        {"question": "Which gas turns limewater milky?", "options": ["Oxygen", "Hydrogen", "Carbon (IV) oxide", "Nitrogen"], "answer": "Carbon (IV) oxide"},
        {"question": "The process of separation of mixtures based on boiling points is called:", "options": ["Filtration", "Fractional distillation", "Evaporation", "Chromatography"], "answer": "Fractional distillation"}
    ],
    "Biology": [
        {"question": "Which organelle is known as the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"], "answer": "Mitochondria"},
        {"question": "The ultimate source of energy for all ecosystems is:", "options": ["Green plants", "The Sun", "Water", "Soil nutrients"], "answer": "The Sun"},
        {"question": "Which of the following blood groups is known as the universal donor?", "options": ["Group A", "Group B", "Group AB", "Group O"], "answer": "Group O"},
        {"question": "The mammalian kidney is the primary organ for:", "options": ["Digestion", "Respiration", "Excretion & Osmoregulation", "Circulation"], "answer": "Excretion & Osmoregulation"}
    ],
    "Civic Education": [
        {"question": "Which of the following is a key characteristic of democracy?", "options": ["Rule of Law", "Dictatorship", "Monarchy", "Military Rule"], "answer": "Rule of Law"},
        {"question": "Fundamental Human Rights are usually enshrined in the:", "options": ["Constitution", "Police Act", "Penal Code", "By-laws"], "answer": "Constitution"},
        {"question": "A major consequence of political apathy in a society is:", "options": ["Good governance", "Poor leadership selection", "Economic boom", "Peace and order"], "answer": "Poor leadership selection"}
    ],
    "Digital Technology": [
        {"question": "What does CPU stand for?", "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Control Program Unit"], "answer": "Central Processing Unit"},
        {"question": "Which of these is an example of an operating system?", "options": ["Microsoft Word", "Python", "Windows", "Google Chrome"], "answer": "Windows"},
        {"question": "The brain of the computer is the:", "options": ["RAM", "Hard Drive", "CPU", "Monitor"], "answer": "CPU"},
        {"question": "Which network topology connects all devices to a central hub or switch?", "options": ["Bus topology", "Ring topology", "Star topology", "Mesh topology"], "answer": "Star topology"}
    ],
    "Economics": [
        {"question": "What happens to demand when price increases (holding other factors constant)?", "options": ["Increases", "Decreases", "Remains Constant", "Fluctuates"], "answer": "Decreases"},
        {"question": "Opportunity cost can be defined as:", "options": ["Money spent on goods", "Real cost expressed in terms of forgone alternatives", "Total cost of production", "Government tax"], "answer": "Real cost expressed in terms of forgone alternatives"},
        {"question": "Inflation caused by excessive aggregate demand over supply is called:", "options": ["Cost-push inflation", "Demand-pull inflation", "Imported inflation", "Structural inflation"], "answer": "Demand-pull inflation"}
    ],
    "Geography": [
        {"question": "Which layer of the atmosphere contains the ozone layer?", "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"], "answer": "Stratosphere"},
        {"question": "Lines drawn on a map joining places of equal pressure are called:", "options": ["Contours", "Isobars", "Isotherms", "Isohyets"], "answer": "Isobars"},
        {"question": "The instrument used to measure atmospheric pressure is the:", "options": ["Thermometer", "Barometer", "Anemometer", "Rain gauge"], "answer": "Barometer"}
    ]
}

# --- FLEXIBLE LOGIN SYSTEM ---
st.sidebar.title("🔐 Portal Login")
role = st.sidebar.selectbox("Select Login Role", ["Student", "Teacher / Admin"])
username = st.sidebar.text_input("Enter Your Name")
password = st.sidebar.text_input("Enter Any Password", type="password")

if not username or not password:
    st.warning("⚠️ Please enter your name and any password to log in.")
    st.stop()

st.sidebar.success(f"Logged in as **{username}** ({role})")

# --- TEACHER / ADMIN VIEW ---
if role == "Teacher / Admin":
    st.title("🎓 Student Result Management System (Teacher Portal)")
    st.write(f"Welcome, Teacher **{username}**! Enter assessment scores, compute rankings, and manage student results.")

    st.header("📌 Add Student Record")
    with st.form("student_form", clear_on_submit=True):
        student_name = st.text_input("Student's Full Name")
        
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
                
            subject_scores[sub] = cw + hw + ca + exam

        submitted = st.form_submit_button("Save Student Record")

    if submitted:
        if not student_name.strip():
            st.error("Please enter the student's full name.")
        else:
            grand_total = sum(subject_scores.values())
            average = grand_total / len(subjects)
            record = {"Name": student_name.strip(), "Total Score": grand_total, "Average (%)": round(average, 2)}
            record.update(subject_scores)
            st.session_state.student_records.append(record)
            st.success(f"Record saved for **{student_name}**!")

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

# --- STUDENT VIEW ---
else:
    st.title("📚 Student Portal & WAEC Practice Hub")
    st.write(f"Welcome, **{username}**! Practice multiple WAEC past questions, check your scores, and test your exam readiness.")

    tab1, tab2 = st.tabs(["📝 WAEC Past Questions Practice", "📊 View My Results"])

    with tab1:
        st.header("Interactive WAEC Practice Quiz")
        selected_sub = st.selectbox("Select Subject to Practice:", subjects, key="student_sub_select")
        
        q_list = waec_questions[selected_sub]
        
        if "last_sub" not in st.session_state or st.session_state.last_sub != selected_sub:
            st.session_state.last_sub = selected_sub
            st.session_state.q_idx = 0

        q_idx = st.session_state.q_idx
        q_data = q_list[q_idx]

        st.markdown(f"### Question {q_idx + 1} of {len(q_list)} ({selected_sub})")
        st.info(q_data['question'])
        
        user_choice = st.radio("Choose your answer:", q_data["options"], key=f"q_choice_{selected_sub}_{q_idx}")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Submit Answer", key=f"sub_ans_{selected_sub}_{q_idx}"):
                st.session_state.quiz_total += 1
                if user_choice == q_data["answer"]:
                    st.session_state.quiz_score += 1
                    st.success("🎉 Correct Answer! Great job.")
                else:
                    st.error(f"❌ Incorrect. The correct answer is: **{q_data['answer']}**")
        
        with col_btn2:
            if st.button("Next Question ➡️", key=f"next_q_{selected_sub}_{q_idx}"):
                if st.session_state.q_idx < len(q_list) - 1:
                    st.session_state.q_idx += 1
                    st.rerun()
                else:
                    st.info("You have reached the last question for this subject! Try switching to another subject.")

        st.markdown("---")
        st.metric("Total Quiz Performance", f"{st.session_state.quiz_score} / {st.session_state.quiz_total} Correct")

    with tab2:
        st.header("Your Saved Academic Records")
        if not st.session_state.student_records:
            st.info("No records found in the system yet. Ask your teacher to upload your scores!")
        else:
            df = pd.DataFrame(st.session_state.student_records)
            student_df = df[df["Name"].str.lower() == username.lower()]
            if student_df.empty:
                st.warning(f"No records found matching the name '{username}'. Check with your teacher.")
            else:
                st.success(f"Found records for **{username}**!")
                st.dataframe(student_df, use_container_width=True)
