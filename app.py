from flask import Flask, render_template, request, redirect, url_for, flash
import os
from models import db
import database as db_ops
import validators

app = Flask(__name__)
app.secret_key = 'sekretny_klucz_do_flash'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    doctors_list = ["Dr Janusz Kardiolog", "Dr Anna Okulista", "Dr Piotr Chirurg"]
    return render_template('index.html', doctors=doctors_list)

@app.route('/book', methods=['POST'])
def book():
    data = {
        'doctor': request.form.get('doctor'),
        'visit_date': request.form.get('visit_date'),
        'patient_name': request.form.get('patient_name'),
        'gender': request.form.get('gender'),
        'pesel': request.form.get('pesel'),
        'birth_date': request.form.get('birth_date'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email'),
        'address': request.form.get('address')
    }

    if not all(data.values()):
        flash("Wszystkie pola formularza są wymagane!", "error")
        return redirect(url_for('index'))

    if not validators.validate_pesel(data['pesel']):
        flash("Nieprawidłowy numer PESEL (błędna długość lub cyfra kontrolna).", "error")
        return redirect(url_for('index'))

    dates_valid, date_msg = validators.validate_dates(data['visit_date'], data['birth_date'])
    if not dates_valid:
        flash(date_msg, "error")
        return redirect(url_for('index'))

    if not validators.validate_phone(data['phone']):
        flash("Nieprawidłowy numer telefonu (wymagane 9 cyfr).", "error")
        return redirect(url_for('index'))

    if not validators.validate_email(data['email']):
        flash("Nieprawidłowy adres email.", "error")
        return redirect(url_for('index'))

    if db_ops.is_slot_taken(data['doctor'], data['visit_date']):
        flash(f"Termin {data['visit_date'].replace('T', ' ')} jest już zajęty!", "error")
        return redirect(url_for('index'))

    db_ops.create_appointment(data)

    flash("Wizyta zarejestrowana pomyślnie!", "success")
    return redirect(url_for('appointments_list'))

@app.route('/list')
def appointments_list():
    visits = db_ops.get_all_appointments()
    return render_template('list.html', visits=visits)

@app.route('/delete/<int:id>')
def delete(id):
    db_ops.delete_appointment(id)
    flash("Wizyta usunięta.", "info")
    return redirect(url_for('appointments_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)