import os 
import certifi 

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
user = os.environ.get("MONGODB_USER")

def create_mongo_client() -> MongoClient:

    if not user or not password:
        raise RuntimeError(
            "MONGODB_USER and MONGODB_PWD must be set"
        )

    uri = f"mongodb+srv://{user}:{password}@cluster0.svd711w.mongodb.net/"

    return MongoClient(
        uri,
        server_api = ServerApi("1"),
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS = 5000, 
    )