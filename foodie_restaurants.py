from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId

from models import RestaurantCreate, RestaurantUpdate
from foodieSchemas import individual_data, list_data


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


# Eλεγχος MongoDB ObjectId

def validate_id(id: str) -> ObjectId:

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=400,
            detail="Μη έγκυρο ObjectId format"
        )

    return ObjectId(id)


# GET - Όλα τα εστιατόρια

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
        query["name"] = {
            "$regex": search,
            "$options": "i"
        }

    collection = request.app.state.restaurants

    total_docs = collection.count_documents(query)

    cursor = (
        collection.find(query)
        .skip((page - 1) * per_page)
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

    restaurant = request.app.state.restaurants.find_one(
        {"_id": object_id}
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Το εστιατόριο δεν βρέθηκε"
        )

    return individual_data(restaurant)


# POST 

@router.post("/", status_code=201)
def create_restaurant(
    request: Request,
    new_restaurant: RestaurantCreate
):

    collection = request.app.state.restaurants

    data = new_restaurant.model_dump()

    result = collection.insert_one(data)

    return {
        "status": "success",
        "id": str(result.inserted_id)
    }


# PUT 

@router.put("/{id}")
def update_restaurant(
    id: str,
    request: Request,
    updated_restaurant: RestaurantCreate
):

    object_id = validate_id(id)

    collection = request.app.state.restaurants

    result = collection.update_one(
        {"_id": object_id},
        {
            "$set": updated_restaurant.model_dump()
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Το εστιατόριο δεν βρέθηκε"
        )

    restaurant = collection.find_one(
        {"_id": object_id}
    )

    return individual_data(restaurant)


# PATCH 

@router.patch("/{id}")
def patch_restaurant(
    id: str,
    request: Request,
    changes: RestaurantUpdate
):

    object_id = validate_id(id)

    collection = request.app.state.restaurants

    update_data = changes.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Δεν δόθηκαν πεδία για ενημέρωση"
        )

    result = collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Το εστιατόριο δεν βρέθηκε"
        )

    restaurant = collection.find_one(
        {"_id": object_id}
    )

    return individual_data(restaurant)


# DELETE 

@router.delete("/{id}")
def delete_restaurant(
    id: str,
    request: Request
):

    object_id = validate_id(id)

    result = request.app.state.restaurants.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Το εστιατόριο δεν βρέθηκε"
        )

    return {
        "message": "Διαγράφηκε επιτυχώς"
    }