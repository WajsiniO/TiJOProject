from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'sekretny_klucz_do_flash'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route('/')
def index():
    doctors_list = ["Dr Janusz Kardiolog", "Dr Anna Okulista", "Dr Piotr Chirurg"]
    return render_template('index.html', doctors=doctors_list)

@app.route('/book', methods=['POST'])
def book():
    doctor = request.form.get('doctor')
    visit_date = request.form.get('visit_date')
    patient_name = request.form.get('patient_name')
    gender = request.form.get('gender')
    pesel = request.form.get('pesel')
    birth_date = request.form.get('birth_date')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')

    if not all([doctor, visit_date, patient_name, gender, pesel, birth_date, phone, email, address]):
        flash("Wszystkie pola formularza są wymagane!", "error")
        return redirect(url_for('index'))

    existing = Appointment.query.filter_by(doctor=doctor, visit_date=visit_date).first()
    if existing:
        flash(f"Termin {visit_date.replace('T', ' ')} jest już zajęty!", "error")
        return redirect(url_for('index'))

    new_visit = Appointment(
        doctor=doctor,
        visit_date=visit_date,
        patient_name=patient_name,
        gender=gender,
        pesel=pesel,
        birth_date=birth_date,
        phone=phone,
        email=email,
        address=address
    )
    db.session.add(new_visit)
    db.session.commit()

    flash("Wizyta zarejestrowana pomyślnie!", "success")
    return redirect(url_for('appointments_list'))

@app.route('/list')
def appointments_list():
    visits = Appointment.query.order_by(Appointment.visit_date).all()
    return render_template('list.html', visits=visits)

@app.route('/delete/<int:id>')
def delete(id):
    visit = Appointment.query.get_or_404(id)
    db.session.delete(visit)
    db.session.commit()
    flash("Wizyta usunięta.", "info")
    return redirect(url_for('appointments_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)