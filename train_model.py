import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

def save_model(model, feature_names, class_names, filename="id3_model.joblib"):
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)

    # Attach attributes to model
    model.feature_names = feature_names
    model.class_names = class_names.tolist()  # Ensure it's JSON-serializable

    # Save model
    joblib.dump(model, models_dir / filename, protocol=4)
    print(f"✅ Model saved to: {models_dir / filename}")
    return models_dir / filename

def train():
    # Load and verify dataset
    data_path = Path(__file__).parent.parent / "data" / "cleaned_medical_data.csv"
    df = pd.read_csv(data_path)

    if 'Diagnosis' not in df.columns:
        raise ValueError("Data must contain a 'Diagnosis' column")

    X = df.drop(columns=['Diagnosis'])

    # Encode class labels
    le = LabelEncoder()
    y = le.fit_transform(df['Diagnosis'])

    # Save label encoder
    models_dir = Path(__file__).parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    joblib.dump(le, models_dir / "label_encoder.joblib", protocol=4)
    print(f"✅ Label encoder saved to: {models_dir / 'label_encoder.joblib'}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # Train model
    model = DecisionTreeClassifier(criterion="entropy", max_depth=3)
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    accuracy = np.mean(predictions == y_test)
    print(f"🧪 Accuracy: {accuracy:.2%}")

    # Save model
    save_model(model, X.columns.tolist(), le.classes_)

if __name__ == "__main__":
    try:
        train()
    except Exception as e:
        print(f"❌ Training failed: {e}")
