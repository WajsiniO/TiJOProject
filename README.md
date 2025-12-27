# System Rejestracji Pacjentów (TiJO Project)

Aplikacja internetowa stworzona w ramach projektu z przedmiotu "Testowanie i Jakość Oprogramowania". System umożliwia pacjentom umawianie wizyt lekarskich, przeglądanie zarezerwowanych terminów oraz ich usuwanie, z pełną walidacją danych wejściowych.

## Funkcjonalności

*   **Rejestracja wizyty:** Formularz umożliwiający wybór lekarza, daty wizyty oraz podanie danych osobowych.
*   **Zaawansowana walidacja danych:**
    *   **PESEL:** Sprawdzanie poprawności cyfry kontrolnej oraz długości (11 cyfr).
    *   **Daty:** Weryfikacja czy data wizyty jest w przyszłości, a data urodzenia w przeszłości.
    *   **Unikalność terminów:** Blokada możliwości umówienia dwóch wizyt u tego samego lekarza w tym samym czasie.
    *   **Dane kontaktowe:** Walidacja formatu adresu e-mail oraz numeru telefonu (9 cyfr).
*   **Zarządzanie wizytami:** Możliwość podglądu listy wszystkich wizyt oraz ich usuwania.
*   **Baza danych:** Dane przechowywane są w lokalnej bazie SQLite.

## Struktura Projektu

Projekt został podzielony na moduły zgodnie z zasadami czystego kodu:

*   `app.py`: Główny plik aplikacji Flask, obsługujący routing.
*   `models.py`: Definicja modelu bazy danych (`Appointment`).
*   `database.py`: Logika biznesowa i operacje na bazie danych (CRUD).
*   `validators.py`: Funkcje walidujące dane wejściowe (PESEL, daty, email, telefon).
*   `tests/`: Katalog zawierający testy jednostkowe.
*   `templates/`: Szablony HTML (`index.html`, `list.html`).
*   `static/`: Pliki statyczne (CSS).

## Instalacja i Uruchomienie

### Wymagania

*   Python 3.x
*   Biblioteki: `Flask`, `Flask-SQLAlchemy`

### Instrukcja krok po kroku

1.  **Instalacja zależności:**
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```

2.  **Uruchomienie aplikacji:**
    ```bash
    python app.py
    ```
    Aplikacja będzie dostępna pod adresem: `http://127.0.0.1:5000/`

    *Podczas pierwszego uruchomienia plik bazy danych `database.db` zostanie utworzony automatycznie.*

## Testowanie

Projekt posiada zestaw testów jednostkowych napisanych przy użyciu modułu `unittest`. Testy weryfikują poprawność działania aplikacji, w tym walidację formularzy i obsługę bazy danych.

Aby uruchomić testy, wykonaj polecenie w głównym katalogu projektu:

```bash
python -m unittest discover tests
```

### Zakres testów
Testy (`tests/test_app.py`) obejmują m.in.:
*   Poprawność ładowania stron.
*   Scenariusze pozytywne rezerwacji.
*   Weryfikację blokady duplikatów terminów.
*   Walidację błędnych numerów PESEL (długość, suma kontrolna).
*   Walidację dat (przeszłość/przyszłość).
*   Walidację formatu e-mail i telefonu.
*   Usuwanie wizyt.