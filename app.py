import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "How often do you feel mentally exhausted after completing your daily activities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How frequently do you feel motivated to complete your academic tasks?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you lose focus while studying or working?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How well do you manage your emotions during stressful situations?",
     "opts": [("Very well",0),("Well",1),("Neutral",2),("Poorly",3),("Very poorly",4)]},
    {"q": "How often do you feel isolated from peers?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you feel pressure due to academic responsibilities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How frequently do you feel satisfied with your daily productivity?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you feel tired even after getting enough rest?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How confident do you feel about your academic future?",
     "opts": [("Very confident",0),("Confident",1),("Neutral",2),("Not confident",3),("Not confident at all",4)]},
    {"q": "How often do deadlines make you feel overwhelmed?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you find it difficult to relax after studying?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you feel emotionally stable during the week?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you feel nervous before exams or presentations?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you enjoy your daily routine?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you feel overwhelmed by your thoughts? ",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]}
    {"q": "How often do you feel positive about your personal life?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Always",4)]}

]

psych_states = {
    "Excellent Mental State": (0, 15),
    "Good Condition": (16, 30),
    "Mild Stress": (31, 45),
    "Moderate Stress": (46, 60),
    "High Stress": (61, 75),
    "Very High Stress": (76, 90),
    "Critical Condition": (91, 100)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Student Psychological Survey")
st.title("📝 Student Psychological Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
