import streamlit as st
import pickle

# Loading trained model
model = pickle.load(open("model.pkl", "rb"))
st.title("🎓 Student Placement Prediction")

st.write("Enter student's CGPA and IQ to check if you might get placed.")

# Take inputs

cgpa = st.number_input("CGPA (0 - 10)", min_value=0.0, max_value=10.0, step=0.1)
iq = st.number_input("IQ (0 - 100)", min_value=50, max_value=200, step=1)

if st.button("Predict"):
    # Make prediction
    prediction = model.predict([[cgpa, iq]])[0]

    if prediction == 1:
        st.success("✅ Congratulations! You are likely to get placed.")
    else:
        st.error("❌ You might not get placed. Keep improving!")
