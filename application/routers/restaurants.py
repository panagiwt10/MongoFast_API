from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId

from appSchemas import individual_data, list_data

router = APIRouter(
    prefix="/restaurants", 
    tags=["Restaurants"]
)

# ελεγχος για MongoDB ObjectID
def validate_id(id:str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code = 400,
            detail="Μη έγκυρο ObjectId format"
        )
    return ObjectId(id)

# GET - Όλα τα εστιατόρια με σελιδοποίηση και φίλτρα
@router.get("/")
def get_restaurants(
    request: Request,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    borough: str | None = None,
    cuisine: str | None = None,
    search: str | None = None,
):
    collection = request.app.state.restaurants
    query = {}
    if borough:
        query["borough"] = borough
    if cuisine:
        query["cuisine"] = cuisine
    if search:
        query["name"] = {
            "$regex": search,
            "$options": "i"
        }

    total_docs = collection.count_documents(query)

    cursor = (
       collection.find(query).skip((page - 1) * per_page)
        .limit(per_page)
    )

    raw_data = list(cursor)

    return {
        "page": page,
        "per_page": per_page,
        "total": total_docs,
        "items": list_data(raw_data),
    }

# GET - Ένα εστιατόριο με ID
@router.get("/{id}")
def get_single_restaurant(
    id: str,
    request: Request
):
    object_id = validate_id(id)
    collection = request.app.state.restaurants

    restaurant = collection.find_one({"_id": object_id})

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Το εστιατόριο δεν βρέθηκε"
        )

    return individual_data(restaurant)