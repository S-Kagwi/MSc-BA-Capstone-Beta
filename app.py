import streamlit as st
import pandas as pd
import pickle

# Load the trained model
model = pickle.load(open('finalized_model.pkl', 'rb'))

# Main function for Streamlit app
def main():
    st.title("Hypertension Prediction WebApp")

    # User inputs with descriptive text
    age = st.number_input("What is your age?", min_value=0, max_value=100, step=1)
    gender = st.selectbox("What is your gender?", ['Male', 'Female'])
    smoking = st.selectbox("Do you smoke?", ['No', 'Yes'])
    alcohol_consumption = st.selectbox("Do you consume alcohol?", ['No', 'Yes'])
    obesity = st.selectbox("Are you obese?", ['No', 'Yes'])
    family_history = st.selectbox("Does your family have a history of hypertension?", ['No', 'Yes'])
    diabetes = st.selectbox("Do you have diabetes?", ['No', 'Yes'])
    salt_intake = st.selectbox("How would you consider the level of your salt intake?", ['Low', 'High'])
    diet = st.selectbox("How would you consider your diet to be?", ['Healthy','Unhealthy'])
    stress_level = st.selectbox("Is your level of stress high or low?", ['Low', 'High'])
    country = st.selectbox("Which country do you belong to?", ['South Africa', 'Nigeria'])

    # Prepare input data for prediction
    input_features = {
        'AGE': age,
        'GENDER': 0 if gender == 'Male' else 1,
        'SMOKING': 1 if smoking == 'Yes' else 0,
        'ALCOHOL_CONSUMPTION': 1 if alcohol_consumption == 'Yes' else 0,
        'OBESITY': 1 if obesity == 'Yes' else 0,
        'FAMILY_HISTORY': 1 if family_history == 'Yes' else 0,
        'DIABETES': 1 if diabetes == 'Yes' else 0,
        'SALT_INTAKE': 1 if salt_intake == 'Yes' else 0,
        'DIET': {'Healthy': 0,'Unhealthy': 1}[diet],
        'STRESS_LEVEL': {'Low': 0,'High': 1}[stress_level],
        'COUNTRY': 0 if country == 'South Africa' else 1
    }

    # Prediction button
    if st.button('Predict Hypertension'):
        input_df = pd.DataFrame([input_features])
        prediction = model.predict(input_df)

        if prediction[0] == 1:
            st.success('The user is likely to be having hypertension.')
        else:
            st.success('The user is not likely to be having hypertension.')

if __name__ == '__main__':
    main()
