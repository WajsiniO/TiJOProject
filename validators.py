from datetime import datetime
import re

def validate_pesel(pesel):
    if not pesel.isdigit() or len(pesel) != 11:
        return False
    
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = 0
    for i in range(10):
        checksum += int(pesel[i]) * weights[i]
    
    last_digit = checksum % 10
    control_digit = (10 - last_digit) % 10
    
    return control_digit == int(pesel[10])

def validate_dates(visit_date_str, birth_date_str):
    """
    Returns a tuple (bool, str). 
    True if valid, False if invalid. 
    String contains error message.
    """
    try:
        # visit_date format from datetime-local input: 'YYYY-MM-DDTHH:MM'
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%dT%H:%M')
        # birth_date format from date input: 'YYYY-MM-DD'
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    except ValueError:
        return False, "Nieprawidłowy format daty."

    now = datetime.now()

    if visit_date < now:
        return False, "Data wizyty nie może być z przeszłości."

    if birth_date > now:
        return False, "Data urodzenia nie może być z przyszłości."

    return True, ""

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 9

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None