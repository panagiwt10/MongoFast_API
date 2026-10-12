import os 
import certifi
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv)

password = os.environ.get("MONGODB_PWD")
user = os.environ.get("MONGODB_USER")

uri = f"mongodb+srv://{user}:{password}@cluster0.svd711w.mongodb.net/"
client = MongoClient(
    uri,
    tlsCAFile = certifi.where(),
    serverSelectiontimeoutMS=5000, 
)

db = client.sample_restaurants
collection = db.restaurants