import unittest
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, Appointment

class AppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_valid_data(self):
        future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M')
        # Valid PESEL: 90090515836
        return {
            'doctor': 'Dr Janusz Kardiolog',
            'visit_date': future_date,
            'patient_name': 'Test Pacjent',
            'gender': 'Mężczyzna',
            'pesel': '90090515836',
            'birth_date': '1990-09-05',
            'phone': '123456789',
            'email': 'test@test.com',
            'address': 'Testowa 1'
        }

    # 1. Strona główna
    def test_index_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dr Janusz Kardiolog', response.data)

    # 2. Poprawne umówienie wizyty
    def test_book_valid_appointment(self):
        data = self.get_valid_data()
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wizyta zarejestrowana', response.data)
        self.assertEqual(Appointment.query.count(), 1)

    # 3. Blokada duplikatu terminu
    def test_book_duplicate_appointment(self):
        data = self.get_valid_data()
        self.app.post('/book', data=data, follow_redirects=True)
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'jest ju', response.data)
        self.assertEqual(Appointment.query.count(), 1)

    # 4. Data wizyty w przeszłości
    def test_book_past_visit_date(self):
        data = self.get_valid_data()
        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        data['visit_date'] = past_date
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Data wizyty nie', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 5. Data urodzenia w przyszłości
    def test_book_future_birth_date(self):
        data = self.get_valid_data()
        future_birth = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        data['birth_date'] = future_birth
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Data urodzenia nie', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 6. Nieprawidłowa długość PESEL
    def test_book_invalid_pesel_length(self):
        data = self.get_valid_data()
        data['pesel'] = '123'
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Nieprawid', response.data)
        self.assertIn(b'PESEL', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 7. Błędna cyfra kontrolna PESEL
    def test_book_invalid_pesel_control_digit(self):
        data = self.get_valid_data()
        data['pesel'] = '90090515835' # Invalid checksum
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Nieprawid', response.data)
        self.assertIn(b'PESEL', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 8. Błędny numer telefonu
    def test_book_invalid_phone(self):
        data = self.get_valid_data()
        data['phone'] = 'abc'
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Nieprawid', response.data)
        self.assertIn(b'telefonu', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 9. Błędny email
    def test_book_invalid_email(self):
        data = self.get_valid_data()
        data['email'] = 'niepoprawnyemail'
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Nieprawid', response.data)
        self.assertIn(b'email', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 10. Brakujące pole
    def test_book_missing_fields(self):
        data = self.get_valid_data()
        del data['doctor']
        
        response = self.app.post('/book', data=data, follow_redirects=True)
        self.assertIn(b'Wszystkie pola', response.data)
        self.assertEqual(Appointment.query.count(), 0)

    # 11. Listowanie
    def test_list_appointments(self):
        data = self.get_valid_data()
        self.app.post('/book', data=data)
        
        response = self.app.get('/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['patient_name'].encode('utf-8'), response.data)

    # 12. Usuwanie
    def test_delete_appointment(self):
        data = self.get_valid_data()
        appt = Appointment(**data)
        db.session.add(appt)
        db.session.commit()
        
        response = self.app.get(f'/delete/{appt.id}', follow_redirects=True)
        self.assertIn(b'Wizyta usuni', response.data)
        self.assertIsNone(Appointment.query.get(appt.id))

if __name__ == "__main__":
    unittest.main()
