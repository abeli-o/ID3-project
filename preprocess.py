import pandas as pd
import os

def preprocess(raw_path, clean_path):
    """Remove duplicates and save cleaned data."""
    df = pd.read_csv(raw_path)
    initial_rows = len(df)
    
    # Cleanup
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)
    
    # Save cleaned data
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    
    print(f"Removed {initial_rows - len(df)} duplicates. Saved to {clean_path}")
    return df

if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_path = os.path.join(PROJECT_ROOT, "health_diagnosis", "data", "balanced_medical_data.csv")
    clean_path = os.path.join(PROJECT_ROOT, "health_diagnosis", "data", "cleaned_medical_data.csv")
    
    preprocess(raw_path, clean_path)