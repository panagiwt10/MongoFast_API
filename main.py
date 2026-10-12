from contextlib import asynccontextmanager

from fastapi import FastAPI
from config_mainFast import create_mongo_client
from foodie_restaurants import router as restaurant_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = create_mongo_client()
    try:
        client.admin.command("ping")
        app.state.restaurants = client.sample_restaurants.restaurants
        yield
    finally:
        client.close()

app = FastAPI(
    title="Foodie Discovery API",
    description="Async API για αναζήτηση και διαχείριση εστιατορίων με FastAPI & MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(restaurant_router)


@app.get("/")
def health_check():
    return {"status": "online", "message": "Welcome to Foodie API"}