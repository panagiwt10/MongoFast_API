# 🍽️ Foodie Matchmaking API

Ένα απλό REST API για αναζήτηση εστιατορίων και σύγκριση προτιμήσεων χρηστών. Είναι φτιαγμένο με **FastAPI** και **MongoDB Atlas**.

## ✨ Τι κάνει

- Εμφανίζει εστιατόρια με σελιδοποίηση.
- Αναζητά εστιατόρια με βάση το όνομα, την περιοχή (`borough`) ή την κουζίνα (`cuisine`).
- Δημιουργεί ή ενημερώνει χρήστες και τις προτιμήσεις τους.
- Υπολογίζει το ποσοστό ταιριάσματος δύο χρηστών από τα εστιατόρια που έχουν κάνει like.
- Εμφανίζει τα κοινά αγαπημένα εστιατόρια των δύο χρηστών.

## 🛠️ Τεχνολογίες

Python · FastAPI · MongoDB Atlas · PyMongo · Pydantic · Uvicorn

## 🚀 Εγκατάσταση και εκτέλεση

**1. Κατέβασε το project και μπες στον φάκελο `application`:**

```bash
git clone https://github.com/panagiwt10/MongoFast_API.git
cd MongoFast_API/application
```

**2. Δημιούργησε ένα virtual environment (προαιρετικά):**

```bash
python -m venv .venv
```

Ενεργοποίησέ το σε Linux/macOS:

```bash
source .venv/bin/activate
```

ή σε Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

**3. Εγκατάστησε τις εξαρτήσεις:**

```bash
pip install -r requirements.txt
```

**4. Δημιούργησε αρχείο `.env` στον φάκελο `application`:**

```env
MONGODB_USER=your_username
MONGODB_PWD=your_password
```

Χρειάζεσαι πρόσβαση σε MongoDB Atlas, στο cluster που έχει οριστεί στο `database.py`, και στη βάση `sample_restaurants` με συλλογή `restaurants`. Η συλλογή `users` χρησιμοποιείται για τα στοιχεία χρηστών. **Μην ανεβάζεις το `.env` στο GitHub.**

**5. Ξεκίνα το API:**

```bash
uvicorn main:app --reload
```

Άνοιξε το **http://127.0.0.1:8000/docs** για να δοκιμάσεις τα endpoints από το Swagger UI.

## 📌 Endpoints

| Method | Endpoint | Περιγραφή |
| --- | --- | --- |
| `GET` | `/` | Μήνυμα καλωσορίσματος |
| `GET` | `/restaurants/` | Λίστα εστιατορίων με φίλτρα και σελιδοποίηση |
| `GET` | `/restaurants/{id}` | Στοιχεία συγκεκριμένου εστιατορίου |
| `POST` | `/users/` | Δημιουργία ή ενημέρωση χρήστη |
| `POST` | `/users/seed-random-likes` | Δοκιμαστικά likes σε δύο χρήστες |
| `GET` | `/matchmaking/?user1=nikos&user2=panos` | Σύγκριση δύο χρηστών |

### Παράδειγμα αναζήτησης

```http
GET /restaurants/?borough=Manhattan&cuisine=Italian&page=1
```

### Παράδειγμα δημιουργίας χρήστη

`POST /users/`

```json
{
  "username": "nikos",
  "preferences": {
    "cuisine": "Italian",
    "borough": "Manhattan"
  }
}
```

### Παράδειγμα matchmaking

Αρχικά μπορείς να καλέσεις το `POST /users/seed-random-likes` για να δημιουργήσεις δοκιμαστικά likes. Έπειτα:

```http
GET /matchmaking/?user1=nikos&user2=panos
```

Το αποτέλεσμα περιλαμβάνει ποσοστό ταιριάσματος (`match_percentage`) και τη λίστα των κοινών εστιατορίων (`common_restaurants`). Το ποσοστό βασίζεται στα κοινά likes (cosine similarity).

## 📁 Δομή project

```text
application/
├── main.py                 # Εκκίνηση του FastAPI
├── database.py             # Σύνδεση με MongoDB Atlas
├── models.py               # Μοντέλο δεδομένων χρήστη
├── appSchemas.py           # Μορφοποίηση δεδομένων εστιατορίων
├── requirements.txt        # Python dependencies
└── routers/
    ├── restaurants.py      # Αναζήτηση εστιατορίων
    ├── users.py            # Χρήστες και δοκιμαστικά likes
    └── matchmaking.py      # Υπολογισμός ταιριάσματος
```

## 📖 API Documentation

Όσο τρέχει ο server, η διαδραστική τεκμηρίωση είναι διαθέσιμη στο:

**http://127.0.0.1:8000/docs**
