import pandas as pd

def inspect_data(filepath):
    df = pd.read_csv(filepath)
    
    print("=== Data Summary ===")
    print(f"Shape: {df.shape}")
    print("\n=== First 5 Rows ===")
    print(df.head())
    
    print("\n=== Class Distribution ===")
    print(df['Diagnosis'].value_counts())
    
    print("\n=== Feature Correlation ===")
    for col in df.columns[:-1]:  # Exclude target
        if df[col].nunique() == 2:  # Binary features
            ct = pd.crosstab(df[col], df['Diagnosis'])
            print(f"\n{col} vs Diagnosis:")
            print(ct)

if __name__ == "__main__":
    inspect_data("health_diagnosis/data/cleaned_medical_data.csv")