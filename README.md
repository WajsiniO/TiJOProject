# Testowanie i Jakość Oprogramowania

## Autor
Aleksander Wajs

## Temat projektu
System Rejestracji Pacjentów

## Opis projektu
Aplikacja internetowa stworzona w celu umożliwienia pacjentom umawiania wizyt lekarskich, przeglądania zarezerwowanych terminów oraz ich usuwania. Projekt kładzie szczególny nacisk na jakość danych poprzez pełną walidację formularzy wejściowych.

**Główne funkcjonalności:**
* **Rejestracja wizyty:** Formularz umożliwiający wybór lekarza, daty wizyty oraz podanie danych osobowych.
* **Zarządzanie wizytami:** Podgląd listy wizyt oraz możliwość ich odwołania.
* **Zaawansowana walidacja danych:**
    * **PESEL:** Weryfikacja cyfry kontrolnej i długości.
    * **Daty:** Blokada dat przeszłych dla wizyt oraz dat przyszłych dla urodzeń.
    * **Unikalność:** Blokada duplikatów terminów u tego samego lekarza.
    * **Kontakt:** Walidacja formatu e-mail i telefonu.

## Uruchomienie projektu

### Wymagania wstępne
* Python 3.x
* Zainstalowanee biblioteki `Flask`, `Flask-SQLAlchemy`.

### Instrukcja
1.  **Instalacja zależności:**
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```

2.  **Start aplikacji:**
    ```bash
    python app.py
    ```
    Aplikacja uruchomi się pod adresem: `http://127.0.0.1:5000/`.
    *Podczas pierwszego uruchomienia plik bazy danych `database.db` zostanie utworzony automatycznie.*

## Testy
Projekt zawiera testy jednostkowe weryfikujące logikę biznesową, walidatory oraz działanie tras aplikacji.

* **Lokalizacja testów w projekcie:** Katalog `tests/` (główny plik: `tests/test_app.py`).
* **Opis testów:**
    * `test_index_page_loads`: Sprawdzenie, czy strona główna ładuje się poprawnie (kod 200).
    * `test_book_valid_appointment`: Scenariusz pozytywny - poprawne umówienie wizyty.
    * `test_book_duplicate_appointment`: Weryfikacja blokady zapisu na ten sam termin u tego samego lekarza.
    * `test_book_past_visit_date`: Blokada zapisu wizyty z datą z przeszłości.
    * `test_book_future_birth_date`: Blokada podania daty urodzenia z przyszłości.
    * `test_book_invalid_pesel_length`: Odrzucenie numeru PESEL o błędnej długości.
    * `test_book_invalid_pesel_control_digit`: Odrzucenie numeru PESEL z błędną cyfrą kontrolną.
    * `test_book_invalid_phone`: Weryfikacja walidacji numeru telefonu (wymagane 9 cyfr).
    * `test_book_invalid_email`: Weryfikacja walidacji formatu adresu e-mail.
    * `test_book_missing_fields`: Sprawdzenie, czy system blokuje formularze z brakującymi danymi.
    * `test_list_appointments`: Weryfikacja poprawnego wyświetlania listy zarejestrowanych wizyt.
    * `test_delete_appointment`: Sprawdzenie funkcjonalności usuwania wizyty z systemu.

**Uruchomienie testów:**
```bash
python -m unittest discover tests
```

## Dokumentacja API

Aplikacja udostępnia następujące endpointy:

### 1. Strona Główna / Formularz
*   **URL:** `/`
*   **Metoda:** `GET`
*   **Opis:** Wyświetla stronę główną z formularzem rejestracji wizyty oraz listą dostępnych lekarzy.

### 2. Rejestracja Wizyty
*   **URL:** `/book`
*   **Metoda:** `POST`
*   **Opis:** Przetwarza dane z formularza rejestracji. Waliduje dane i zapisuje wizytę w bazie.
*   **Parametry formularza:**
    *   `doctor`: Imię i nazwisko lekarza.
    *   `visit_date`: Data i godzina wizyty.
    *   `patient_name`: Imię i nazwisko pacjenta.
    *   `gender`: Płeć pacjenta.
    *   `pesel`: Numer PESEL (11 cyfr).
    *   `birth_date`: Data urodzenia.
    *   `phone`: Numer telefonu (9 cyfr).
    *   `email`: Adres e-mail.
    *   `address`: Adres zamieszkania.
*   **Odpowiedź:** Przekierowanie na stronę główną (w przypadku błędu) lub listę wizyt (sukces) z odpowiednim komunikatem `flash`.

### 3. Lista Wizyt
*   **URL:** `/list`
*   **Metoda:** `GET`
*   **Opis:** Wyświetla tabelę ze wszystkimi zarejestrowanymi wizytami.

### 4. Usuwanie Wizyty
*   **URL:** `/delete/<int:id>`
*   **Metoda:** `GET`
*   **Opis:** Usuwa wizytę o podanym identyfikatorze `id`.
*   **Odpowiedź:** Przekierowanie do listy wizyt z komunikatem o usunięciu.

## Przypadki testowe dla testera manualnego (testCase)

Poniżej przedstawiono pełną listę scenariuszy testowych do manualnej weryfikacji aplikacji:

| ID | Nazwa Przypadku | Warunki Wstępne | Kroki Testowe | Oczekiwany Rezultat |
| :--- | :--- | :--- | :--- | :--- |
| **TC_01** | Ładowanie strony głównej | Aplikacja uruchomiona | 1. Otwórz przeglądarkę.<br>2. Wejdź na `http://127.0.0.1:5000/`. | Strona wyświetla się poprawnie, widoczny tytuł i formularz. |
| **TC_02** | Poprawna rejestracja wizyty | Aplikacja uruchomiona | 1. Wypełnij formularz poprawnymi danymi.<br>2. Kliknij "Zarejestruj". | Przekierowanie do listy wizyt. Komunikat: "Wizyta zarejestrowana pomyślnie!". |
| **TC_03** | Duplikat terminu | Istnieje już wizyta w terminie T u lekarza L | 1. Spróbuj zarejestrować nową wizytę u lekarza L w tym samym terminie T.<br>2. Kliknij "Zarejestruj". | Komunikat błędu o zajętym terminie. Wizyta nie zostaje dodana. |
| **TC_04** | Data wizyty w przeszłości | Aplikacja uruchomiona | 1. Wybierz datę wizyty wcześniejszą niż dzisiejsza.<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Data wizyty nie może być z przeszłości". |
| **TC_05** | Data urodzenia w przyszłości | Aplikacja uruchomiona | 1. Wybierz datę urodzenia późniejszą niż dzisiejsza.<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Data urodzenia nie może być z przyszłości". |
| **TC_06** | PESEL - Błędna długość | Aplikacja uruchomiona | 1. Wpisz PESEL krótszy lub dłuższy niż 11 cyfr.<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Nieprawidłowy numer PESEL". |
| **TC_07** | PESEL - Błędna cyfra kontrolna | Aplikacja uruchomiona | 1. Wpisz 11 cyfr PESEL, ale z błędną sumą kontrolną.<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Nieprawidłowy numer PESEL". |
| **TC_08** | Telefon - Błędny format | Aplikacja uruchomiona | 1. Wpisz numer telefonu inny niż 9 cyfr (np. litery lub za krótki).<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Nieprawidłowy numer telefonu". |
| **TC_09** | Email - Błędny format | Aplikacja uruchomiona | 1. Wpisz email bez znaku `@` lub bez domeny.<br>2. Kliknij "Zarejestruj". | Komunikat błędu: "Nieprawidłowy adres email". |
| **TC_10** | Brakujące pola formularza | Aplikacja uruchomiona | 1. Pozostaw dowolne wymagane pole puste.<br>2. Kliknij "Zarejestruj". | Komunikat: "Wszystkie pola formularza są wymagane!". |
| **TC_11** | Wyświetlanie listy wizyt | Istnieją zapisane wizyty | 1. Przejdź do zakładki "Lista wizyt" (`/list`). | Tabela wyświetla wszystkie dane poprawnie zarejestrowanych pacjentów. |
| **TC_12** | Usuwanie wizyty | Na liście istnieje wizyta | 1. Na stronie listy kliknij przycisk "Usuń" przy wybranej wizycie. | Wizyta zostaje usunięta z bazy i znika z tabeli. Komunikat: "Wizyta usunięta". |

## Technologie użyte w projekcie

*   **Język programowania:** Python 3.13
*   **Framework webowy:** Flask
*   **Baza danych:** SQLite (wbudowana)
*   **ORM:** Flask-SQLAlchemy
*   **Frontend:** HTML5, CSS3
*   **Testy:** Unittest (biblioteka standardowa Python)
