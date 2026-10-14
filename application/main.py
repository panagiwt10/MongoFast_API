from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_mongo_client
from routers import matchmaking, restaurants, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = create_mongo_client()
    try:
        client.admin.command("ping")
        database = client.sample_restaurants
        app.state.mongo_client = client
        app.state.restaurants = database.restaurants
        app.state.users = database.users
        yield
    finally:
        client.close()


app = FastAPI(title="Foodie Matchmaking API", lifespan=lifespan)

app.include_router(restaurants.router)
app.include_router(users.router)
app.include_router(matchmaking.router)

@app.get("/")
def home():
    return {"message": "Καλώς ήρθατε στο Foodie API!"}