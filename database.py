# health_diagnosis/src/database.py
# Run the following commands in the terminal to apply migrations:
# flask db migrate -m "Add new fields to Doctor model"
# flask db upgrade
from .schema import db

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        # Drop all tables (only for development!)
        db.drop_all()
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully")