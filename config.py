from pathlib import Path
import os

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODEL_DIR = BASE_DIR / "models"
    
    # Database
    DB_PATH = DATA_DIR / "health.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    
    # Flask Secret Key
    SECRET_KEY = "your-secret-key"  # Replace with a secure random key in production
    
    # Model
    MODEL_PATH = MODEL_DIR / "id3_model.joblib"
    
    @classmethod
    def init_dirs(cls):
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.MODEL_DIR, exist_ok=True)