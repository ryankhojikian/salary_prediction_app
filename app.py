from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel
import os
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Load ML components
model = joblib.load("salary_model.pkl")
encoders = joblib.load("encoders.pkl")

app = FastAPI()

class SalaryRequest(BaseModel):
    experience_level: str
    employment_type: str
    job_title: str
    company_size: str

@app.get("/")
def home():
    return {"status": "Online", "message": "Salary Prediction API is ready!"}

@app.post("/predict")
def predict(data: SalaryRequest):
    # 1. Prepare input for the model
    input_df = pd.DataFrame([data.model_dump()])
    
    # 2. Encode categorical features
    for col, le in encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])
        
    prediction = round(float(model.predict(input_df)[0]), 2)

    # 3. Generate Narrative Insights via Ollama
    story_to_save = "Story generation failed."
    try:
        insight_prompt = f"""You are a senior career advisor. 
        Write a 2-paragraph analysis for a {data.job_title} earning ${prediction:,.2f}.
        Paragraph 1: A brief career narrative about this role.
        Paragraph 2: A specific market insight on how being at a '{data.company_size}' company affects the ${prediction:,.2f} salary for a '{data.experience_level}' level professional.
        Keep it professional."""

        story_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "hf.co/unsloth/Llama-3.2-1B-Instruct-GGUF",
                "prompt": insight_prompt,
                "stream": False
            },
            timeout=20
        )
        
        if story_response.status_code == 200:
            story_to_save = story_response.json().get("response", "No story generated.")
        else:
            story_to_save = f"As a {data.job_title}, your predicted salary is ${prediction:,.2f}."

    except Exception as e:
        print(f"Ollama Error: {e}")
        story_to_save = f"Career outlook for {data.job_title} remains strong at ${prediction:,.2f}."

    # 4. Save to Supabase
    try:
        supabase.table("predictions").insert({
            "job_title": data.job_title,
            "experience_level": data.experience_level,
            "employment_type": data.employment_type,
            "predicted_salary": prediction, # Matches your confirmed table name
            "story": story_to_save  
        }).execute()
        print("Successfully saved to Supabase!")
    except Exception as e:
        print(f"Supabase Error: {e}")
    
    return {
        "predicted_salary_usd": prediction,
        "story": story_to_save,
        "status": "Success"
    }