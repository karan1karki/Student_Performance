import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open("student_pass_prediction.pkl","rb") as model_file:
    model = pickle.load(model_file)
# Title
st.title("🎓 Student Performance Predictor")
st.write("Enter student information to predict if they will pass or fail.")

# Sidebar for user input
gender = st.selectbox("Gender", ["female", "male"])
race = st.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
parent_education = st.selectbox("Parental Education", [
    "some high school", "high school", "some college", 
    "associate's degree", "bachelor's degree", "master's degree"
])
lunch = st.selectbox("Lunch Type", ["standard", "free/reduced"])
test_prep = st.selectbox("Test Preparation", ["none", "completed"])

math_score = st.slider("Math Score", 0, 100, 50)
reading_score = st.slider("Reading Score", 0, 100, 50)
writing_score = st.slider("Writing Score", 0, 100, 50)

# Button
if st.button("Predict"):
    # Feature engineering
    avg_score = np.mean([math_score, reading_score, writing_score])

    # Manual encoding
    gender_map = {"female": 0, "male": 1}
    race_map = {"group A": 0, "group B": 1, "group C": 2, "group D": 3, "group E": 4}
    parent_map = {
        "some high school": 0, "high school": 1, "some college": 2,
        "associate's degree": 3, "bachelor's degree": 4, "master's degree": 5
    }
    lunch_map = {"free/reduced": 0, "standard": 1}
    prep_map = {"none": 0, "completed": 1}

    features = pd.DataFrame([{
        "gender": gender_map[gender],
        "race/ethnicity": race_map[race],
        "parental level of education": parent_map[parent_education],
        "lunch": lunch_map[lunch],
        "test preparation course": prep_map[test_prep],
        "average_score": avg_score
    }])

    # Prediction
    prediction = model.predict(features)[0]
    result = "✅ Pass" if prediction == 1 else "❌ Fail"
    st.subheader(f"Prediction: {result}")
