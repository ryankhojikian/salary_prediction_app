import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Salary Predictor", layout="centered")

st.title("🚀 Career Path AI Predictor")

# Input fields
job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")

col1, col2 = st.columns(2)
with col1:
    experience_level = st.selectbox("Experience Level", options=["EN", "MI", "SE", "EX"])
    employment_type = st.selectbox("Employment Type", options=["FT", "PT", "CT", "FL"])
with col2:
    company_size = st.selectbox("Company Size", options=["S", "M", "L"])

if st.button("Generate My Future"):
    if job_title:
        payload = {
            "job_title": job_title,
            "experience_level": experience_level,
            "employment_type": employment_type,
            "company_size": company_size
        }
        
        with st.spinner("Predicting..."):
            try:
                response = requests.post("http://127.0.0.1:8001/predict", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    user_val = data['predicted_salary_usd']
                    
                    st.divider()
                    st.balloons()
                    
                    # 1. Salary & Short Insight
                    st.success(f"### Predicted Salary: ${user_val:,.2f}")
                    st.info(data['story'])
                    
                    # 2. THE CHART FIX
                    st.markdown("### 📊 Salary Landscape")
                    chart_df = pd.DataFrame({
                        "Category": ["Your Prediction", "Entry Avg", "Executive Avg"],
                        "Salary": [user_val, 65000, 180000] 
                    }).set_index("Category") # This ensures bars show up correctly
                    
                    st.bar_chart(chart_df)

                else:
                    st.error("API Error. Is the backend running?")
            except Exception as e:
                st.error(f"Connection failed: {e}")
    else:
        st.warning("Please enter a Job Title.")