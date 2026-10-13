# Foodie Discovery API

Rest API για αναζητηση κακι διαχειριση. Είναι υλοποιημένο με **FastAPI** και **MongoDB Atlas** και χρησιμοποιεί τη συλλογή `sample_restaurants.restaurants`.

## Δυνατότητες

- Προβολή εστιατοριων με σελιδοποίηση
- Φιλτράρισμα ανά περιοχή (`borough`) και είδος κουζίνας (`cuisine`)
- Αναζήτηση με βάση το όνομα
- Προβολή, δημιουργία, πλήρης ενημέρωση, μερική ενημέρωση και διαγραφή εστιατορίου
- Αυτόματη διαδραστική τεκμηρίωση μέσω Swagger UI

## Τεχνολογίες

- Python
- FastAPI
- MongoDB Atlas
- PyMongo
- Pydantic
- Uvicorn

## Προαπαιτούμενα

- Python 3.10 ή νεότερη
- Λογαριασμός MongoDB Atlas
- Πρόσβαση στη βάση δεδομένων και στο dataset `sample_restaurants`

## Εγκατάσταση

Κλωνοποίησε το repository και μπες στον φάκελό του:

```bash
git clone <repository-url>
cd <repository-folder>
```

## Setup

### 1. create venv 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## Setting MongoDB
Δημιούργησε αρχείο `.env` στον βασικό φάκελο του project και πρόσθεσε τα στοιχεία σύνδεσης του MongoDB Atlas:

```bash
MONGODB_USER=το_username_σου
MONGODB_PWD=το_password_σου

```
## Execute 
```bash
uvicorn main:app --reload
```

## Endpoints
Μέθοδος	Endpoint	Περιγραφή
GET	/	Έλεγχος κατάστασης της API
GET	/restaurants/	Λίστα εστιατορίων με σελιδοποίηση και φίλτρα
GET	/restaurants/{id}	Εμφάνιση εστιατορίου βάσει ID
POST	/restaurants/	Δημιουργία εστιατορίου
PUT	/restaurants/{id}	Πλήρης ενημέρωση εστιατορίου
PATCH	/restaurants/{id}	Μερική ενημέρωση εστιατορίου
DELETE	/restaurants/{id}	Διαγραφή εστιατορίου

## Δομή project
main.py: Δημιουργία της FastAPI εφαρμογής και σύνδεση με το MongoDB.
foodie_restaurants.py: Endpoints για τη διαχείριση εστιατορίων.
models.py: Pydantic models για τα δεδομένα εστιατορίων.
foodieSchemas.py: Μετατροπή εγγράφων MongoDB σε API responses.
config_mainFast.py: Ρύθμιση σύνδεσης με το MongoDB Atlas.
requirements.txt: Εξαρτήσεις Python.
queens_restaurants.json: Αρχείο δεδομένων εστιατορίων.
