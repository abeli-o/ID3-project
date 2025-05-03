from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from health_diagnosis.src.schema import db, User, Diagnosis, Doctor
from health_diagnosis.src.database import init_db
from health_diagnosis.src.config import Config
from health_diagnosis.src.predict import SymptomChecker

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Initialize database and model
init_db(app)
checker = SymptomChecker()



@app.route('/')
def home():
    if 'user_id' not in session:
        flash("Please login to access the dashboard.", "info")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    diagnosis = None
    confidence = None
    
    if request.method == 'POST':
        try:
            # Collect symptoms from the form
            symptoms = {
                feature: 1 if request.form.get(feature) == 'on' else 0
                for feature in checker.required_features
            }
            
            # Predict diagnosis using SymptomChecker
            diagnosis = checker.predict(symptoms)
            confidence = checker.get_confidence(symptoms)
            
            # Format symptoms for display
            active_symptoms = [f.replace('_', ' ') for f, v in symptoms.items() if v == 1]
            symptoms_str = ", ".join(active_symptoms) if active_symptoms else "No symptoms selected"
            
            # Save the diagnosis to the database
            new_diagnosis = Diagnosis(
                user_id=session['user_id'],
                symptoms=symptoms_str,
                diagnosis=diagnosis,
                confidence=confidence,
                date=datetime.utcnow()
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            
            flash(f"Diagnosis: {diagnosis} (Confidence: {confidence:.2f}%)", "success")
        
        except Exception as e:
            db.session.rollback()
            flash(f"Prediction failed: {str(e)}", "error")
    
    return render_template(
        "predict.html",
        symptoms=checker.required_features,
        diagnosis=diagnosis,
        confidence=confidence
    )

# [Previous register, login, logout routes remain the same...]
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash("Please fill out all fields")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    diagnoses = Diagnosis.query.filter_by(
        user_id=session['user_id']
    ).order_by(
        Diagnosis.date.desc()
    ).all()
    
    return render_template('history.html', diagnoses=diagnoses)

@app.route('/doctors', methods=['GET', 'POST'])
def search_doctors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    doctors = []
    specialties = []
    
    # Get unique specialties for dropdown
    specialties = [s[0] for s in db.session.query(Doctor.specialty).distinct().all()]
    
    if request.method == 'POST':
        specialty = request.form.get('specialty')
        location = request.form.get('location')
        
        query = Doctor.query
        
        if specialty and specialty != 'All':
            query = query.filter(Doctor.specialty == specialty)
        
        if location:
            query = query.filter(
                (Doctor.city.ilike(f'%{location}%')) | 
                (Doctor.state.ilike(f'%{location}%'))
            )  # Added this closing parenthesis
        
        doctors = query.order_by(Doctor.rating.desc()).all()
    
    return render_template(
        'doctors.html',
        doctors=doctors,
        specialties=specialties,
        selected_specialty=request.form.get('specialty', ''),
        selected_location=request.form.get('location', '')
    )
@app.cli.command("seed-doctors")
def seed_doctors():
    """Add sample doctors to the database"""
    from health_diagnosis.src.schema import Doctor
    
    sample_doctors = [
        {
            "name": "Dr. Gloria Koech",
            "specialty": "Cardiology",
            "hospital": "City General Hospital",
            "address": "123 Medical Drive",
            "city": "Nairobi",
            "state": "Nairobi",
            "phone": "(555) 123-4567",
            "email": "gloriakoech@citygeneral.org",
            "website": "https://citygeneral.org/cardiology",
            "rating": 4.7,
            "accepts_new_patients": True
        },
        {
            "name": "Dr. Joy Chen",
            "specialty": "Neurology",
            "hospital": "Regional Medical Center",
            "address": "456 Health Avenue",
            "city": "Nakuru",
            "state": "Kenya",
            "phone": "(555) 234-5678",
            "email": "J.chen@regionalmed.org",
            "rating": 4.9,
            "accepts_new_patients": True
        }
    ]

    # Clear existing doctors (optional - uncomment if you want a fresh start)
    Doctor.query.delete()

    #Add new doctors (skip duplicates)
    added = 0
    for doctor_data in sample_doctors:
        if not Doctor.query.filter_by(email=doctor_data["email"]).first():
            db.session.add(Doctor(**doctor_data))
            added += 1

    db.session.commit()
    print(f"✅ Success: Added {added} new doctors")


if __name__ == "__main__":
    app.run(debug=True)