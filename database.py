from models import db, Appointment

def get_all_appointments():
    return Appointment.query.order_by(Appointment.visit_date).all()

def is_slot_taken(doctor, visit_date):
    existing = Appointment.query.filter_by(doctor=doctor, visit_date=visit_date).first()
    return existing is not None

def create_appointment(data):
    new_visit = Appointment(
        doctor=data['doctor'],
        visit_date=data['visit_date'],
        patient_name=data['patient_name'],
        gender=data['gender'],
        pesel=data['pesel'],
        birth_date=data['birth_date'],
        phone=data['phone'],
        email=data['email'],
        address=data['address']
    )
    db.session.add(new_visit)
    db.session.commit()
    return new_visit

def delete_appointment(visit_id):
    visit = Appointment.query.get_or_404(visit_id)
    db.session.delete(visit)
    db.session.commit()
