from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.String(50), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    pesel = db.Column(db.String(11), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
