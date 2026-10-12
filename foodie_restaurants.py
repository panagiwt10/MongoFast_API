from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId
from database.models import RestaurantCreate
from database.schemas import individual_data, list_data

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/")
def get_all_restaurants(
    request: Request,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    borough: str | None = None,
    cuisine: str | None = None,
    search: str | None = None,
):
    query = {}
    if borough:
        query["borough"] = borough
    if cuisine:
        query["cuisine"] = cuisine
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    collection = request.app.state.restaurants
    total_docs = collection.count_documents(query)
    
    cursor = collection.find(query).skip((page - 1) * per_page).limit(per_page)
    raw_data = list(cursor)

    return {
        "page": page,
        "per_page": per_page,
        "total": total_docs,
        "items": list_data(raw_data),
    }


@router.get("/{id}")
def get_single_restaurant(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Μη έγκυρο ObjectId format")

    restaurant = request.app.state.restaurants.find_one({"_id": ObjectId(id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Το εστιατόριο δεν βρέθηκε")

    return individual_data(restaurant)


@router.post("/", status_code=201)
def create_restaurant(request: Request, new_restaurant: RestaurantCreate):
    try:
        collection = request.app.state.restaurants
        data = new_restaurant.model_dump()
        resp = collection.insert_one(data)
        return {"status": "success", "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{id}")
def delete_restaurant(id: str, request: Request):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Μη έγκυρο ObjectId format")

    result = request.app.state.restaurants.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Το εστιατόριο δεν βρέθηκε")

    return {"message": "Διαγράφηκε επιτυχώς"}