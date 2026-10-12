from contextlib import asynccontextmanager

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, APIRouter, HTTPException, Query, Request
from config_mainFast import create_mongo_client
from database.schemas import individual_data, list_data
from database.models import RestaurantCreate, Restau


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = create_mongo_client()
    try:
        client.admin.command("ping")
        app.state.restaurants = client.sample_restaurants.restaurants
        print("Connected successfully")
        yield
    except Exception as exc:
        raise RuntimeError(f"Could not connect to MongoDB Atlas: {exc}") from exc
    finally:
        client.close()


app = FastAPI(lifespan=lifespan)
router = APIRouter()

@router.get("/")
def get_all_restau(
    request: Request,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
):
    collection = request.app.state.restaurants
    data = collection.find().skip((page - 1) * per_page).limit(per_page)
    return {
        "page": page,
        "per_page": per_page,
        "total": collection.count_documents({}),
        "items": list_data(data),
    }


@router.get("/{restaurant_id}", response_model=Restau)
def get_restaurant(restaurant_id: str, request: Request):
    try:
        object_id = ObjectId(restaurant_id)
    except (InvalidId, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid restaurant id") from exc

    restaurant = request.app.state.restaurants.find_one({"_id": object_id})
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return individual_data(restaurant)


@router.post("/")
def create_restaurant(request: Request, new_restaurant: RestaurantCreate):
    try:
        collection = request.app.state.restaurants
        resp = collection.insert_one(new_restaurant.model_dump())
        return {"status_code":200, "id":str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
app.include_router(router)