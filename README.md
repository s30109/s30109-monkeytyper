# 🐒 MonkeyType Mini – Klon gry do szybkiego pisania

Projekt edukacyjny – mini-klon gry MonkeyType z dwiema wersjami:
- 🌐 **Online** – aplikacja webowa z API w Flasku + MongoDB Atlas
- 🖥️ **Offline** – gra konsolowa bez zapisu wyników do bazy

---

## 📦 Wymagania

- Python 3.10+
- Virtualenv (opcjonalnie)
- Konto MongoDB Atlas (do trybu online)

---

## ⚙️ Instalacja

1. **Sklonuj repozytorium lub pobierz pliki**
2. **Utwórz i aktywuj środowisko wirtualne**:

## 🎮 Tryb ONLINE

```

Zainstaluj zależności:
pip install -r requirements.txt
Utwórz plik .env w folderze głównym i dodaj:
MONGO_URI=mongodb+srv://<użytkownik>:<hasło>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<appname>
Upewnij się, że masz plik words.txt z listą słów (jeden wyraz na linię).


Uruchom serwer API:
python api/api.py
Otwórz przeglądarkę i przejdź do:
http://localhost:5000
```
## Funkcje ONLINE:
**Generowanie losowych słów**

**Pomiar WPM, dokładności i czasu**

**Zapis wyników do MongoDB Atlas**

**Podgląd globalnych i użytkownika wyników**

## 🎮 Tryb OFFLINE (konsola)

**python main.py**

## Funkcje:
**30 losowych słów do przepisania**

**Limit czasu: 30 sekund**

**Wynik, WPM i dokładność wyświetlane po zakończeniu**

**Brak zapisu do bazy danych**


## 🧪 Testowanie
**wiele testów jednostkowych**


## 📁 Struktura projektu
<pre>
project_root/
├── api/
│   └── api.py             # Flask REST API
├── database/
│   ├── db.py              # Połączenie z MongoDB Atlas
│   └── models.py          # Operacje na kolekcjach
├── engine/
│   └── core.py            # Logika gry
├── ui/
│   ├── index.html         # Interfejs gry
│   ├── style.css          # Stylizacja gry
│   └── script.js          # Logika gry JS
├── main.py                # Tryb offline (terminal)
├── words.txt              # Lista słów
├── .env                   # Klucz MongoDB Atlas
├── requirements.txt       # Wymagane pakiety
└── README.md              # Ten plik
</pre>