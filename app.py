import streamlit as st
import pandas as pd
import pickle

# Set the page configuration
st.set_page_config(page_title='Hypertension Prediction', page_icon='🩺', layout='wide')

# Inline CSS for styling

st.markdown("""
    <style>
    .reportview-container {
        background-color: #ffeb3b;  /* Bright yellow */
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #03a9f4;  /* Light blue */
    }
    .stButton>button {
        background-color: #8bc34a !important;  /* Light green */
        color: white !important;
        font-size: 20px !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        border: none !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #4caf50 !important;  /* Green */
    }
    </style>
    """, unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        model = pickle.load(open('finalized_model.pkl', 'rb'))
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Function to get user input
def get_user_input():
    st.sidebar.header("Patient's Personal Information and Symptoms")
    
    age = st.sidebar.slider("What is your age?", min_value=0, max_value=100, step=1, key="age")
    gender = st.sidebar.radio("What is your gender?", ['Male', 'Female'], key="gender")
    smoking = st.sidebar.selectbox("Do you smoke?", ['No', 'Yes'], key="smoking")
    alcohol_consumption = st.sidebar.selectbox("Do you consume alcohol?", ['No', 'Yes'], key="alcohol_consumption")
    obesity = st.sidebar.selectbox("Are you obese?", ['No', 'Yes'], key="obesity")
    family_history = st.sidebar.selectbox("Does your family have a history of hypertension?", ['No', 'Yes'], key="family_history")
    diabetes = st.sidebar.selectbox("Do you have diabetes?", ['No', 'Yes'], key="diabetes")
    salt_intake = st.sidebar.radio("How would you consider the level of your salt intake?", ['Low', 'High'], key="salt_intake")
    diet = st.sidebar.radio("How would you consider your diet to be?", ['Healthy', 'Unhealthy'], key="diet")
    stress_level = st.sidebar.radio("Is your level of stress high or low?", ['Low', 'High'], key="stress_level")
    country = st.sidebar.radio("Which country do you belong to?", ['South Africa', 'Nigeria'], key="country")
    
    input_features = {
        'AGE': age,
        'GENDER': 0 if gender == 'Male' else 1,
        'SMOKING': 1 if smoking == 'Yes' else 0,
        'ALCOHOL_CONSUMPTION': 1 if alcohol_consumption == 'Yes' else 0,
        'OBESITY': 1 if obesity == 'Yes' else 0,
        'FAMILY_HISTORY': 1 if family_history == 'Yes' else 0,
        'DIABETES': 1 if diabetes == 'Yes' else 0,
        'SALT_INTAKE': 1 if salt_intake == 'High' else 0,
        'DIET': {'Healthy': 0, 'Unhealthy': 1}[diet],
        'STRESS_LEVEL': {'Low': 0, 'High': 1}[stress_level],
        'COUNTRY': 0 if country == 'South Africa' else 1
    }
    
    return input_features

# Main function for Streamlit app
def main():
    st.title("HyperPredict")
    st.write("This app predicts the likelihood of a user having hypertension based on various health and lifestyle factors.")
    st.image("pic.jpg", use_column_width=True)
    
    input_features = get_user_input()
    
    if st.button('Predict Hypertension'):
        if model:
            input_df = pd.DataFrame([input_features])
            prediction = model.predict(input_df)
            
            if prediction[0] == 1:
                st.success('The user is likely to have hypertension.')
            else:
                st.success('The user is not likely to have hypertension.')
        else:
            st.error("Model not loaded correctly. Please try again later.")

if __name__ == '__main__':
    main()
