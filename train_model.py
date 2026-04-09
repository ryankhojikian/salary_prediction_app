import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder

def train_salary_model(csv_path: str) -> None:
    """Trains a Decision Tree to predict salary based on job data."""
    try:
        # 1. Load the dataset
        df = pd.read_csv(csv_path)
        
        # Normalize job_title to title case for consistency
        df['job_title'] = df['job_title'].str.title()
        
        # 2. Select the Features for the bootcamp project
        features = ['experience_level', 'employment_type', 'job_title', 'company_size']
        X = df[features].copy()
        y = df['salary_in_usd']
        
        # 3. Encoding: Turning words into numbers
        encoders = {}
        for col in features:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
            
        # 4. Training the Decision Tree
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = DecisionTreeRegressor(max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        
        # 5. Save the "Brain" files
        joblib.dump(model, "salary_model.pkl")
        joblib.dump(encoders, "encoders.pkl")
        
        score = model.score(X_test, y_test)
        print(f"✅ Success! Model Score: {score:.2f}")
        print("Created: salary_model.pkl and encoders.pkl")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{csv_path}'. Check your folder!")

if __name__ == "__main__":
    train_salary_model("ds_salaries.csv")