import joblib
import pandas as pd
from pathlib import Path

class SymptomChecker:
    def __init__(self):
        """Initialize the SymptomChecker by loading model and encoder"""
        try:
            current_dir = Path(__file__).parent
            models_dir = current_dir.parent / "models"
            model_path = models_dir / "id3_model.joblib"
            encoder_path = models_dir / "label_encoder.joblib"

            # Verify files exist
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")
            if not encoder_path.exists():
                raise FileNotFoundError(f"Label encoder file not found at {encoder_path}")

            # Load model and encoder
            self.model = joblib.load(model_path)
            self.encoder = joblib.load(encoder_path)
            
            # Get required features from model
            self.required_features = getattr(self.model, 'feature_names_in_', None)
            if self.required_features is None:
                raise ValueError("Model is missing required feature names")

            print("✅ Model and encoder loaded successfully with features:")
            print(", ".join(self.required_features))

        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize SymptomChecker\n"
                f"Error: {str(e)}\n"
                "Solutions:\n"
                "1. Run train_model.py to generate the model and encoder\n"
                "2. Verify they exist in the models directory"
            )

    def predict(self, symptoms):
        """Predict diagnosis from symptoms dictionary
        Args:
            symptoms (dict): Dictionary of symptoms with feature names as keys
        Returns:
            str: Predicted diagnosis
        """
        self._validate_features(symptoms)
        
        input_data = pd.DataFrame(
            [[symptoms[feat] for feat in self.required_features]],
            columns=self.required_features
        )

        class_index = self.model.predict(input_data)[0]
        return self.encoder.inverse_transform([class_index])[0]

    def get_confidence(self, symptoms):
        """Get confidence score for the prediction
        Args:
            symptoms (dict): Dictionary of symptoms with feature names as keys
        Returns:
            float: Confidence percentage (0-100)
        """
        self._validate_features(symptoms)
        
        input_data = pd.DataFrame(
            [[symptoms[feat] for feat in self.required_features]],
            columns=self.required_features
        )

        probabilities = self.model.predict_proba(input_data)[0]
        return max(probabilities) * 100

    def _validate_features(self, symptoms):
        """Validate that all required features are present
        Args:
            symptoms (dict): Dictionary of symptoms to validate
        Raises:
            ValueError: If any required features are missing
        """
        missing = set(self.required_features) - set(symptoms.keys())
        if missing:
            raise ValueError(f"Missing required features: {missing}")

if __name__ == "__main__":
    try:
        checker = SymptomChecker()

        test_symptoms = {
            'Fever': 1,
            'Cough': 0,
            'Fatigue': 1,
            'Headache': 0,
            'Sore_Throat': 0,
            'Shortness_of_Breath': 0,
            'Nausea': 0,
            'Vomiting': 0,
            'Diarrhea': 0,
            'Chest_Pain': 0,
            'Joint_Pain': 0,
            'Loss_of_Appetite': 0,
            'Skin_Rash': 0,
            'Chills': 1,
            'Muscle_Ache': 0,
            'Dizziness': 0,
            'Runny_Nose': 0,
            'Abdominal_Pain': 0
        }

        prediction = checker.predict(test_symptoms)
        confidence = checker.get_confidence(test_symptoms)
        print(f"\nPredicted Diagnosis: {prediction}")
        print(f"Confidence: {confidence:.2f}%")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")