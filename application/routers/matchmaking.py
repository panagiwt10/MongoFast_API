from math import sqrt

from fastapi import APIRouter, HTTPException, Query, Request
from bson import ObjectId


router = APIRouter(
    prefix="/matchmaking",
    tags=["Matchmaking"],
)


def cosine_match_percentage(first_likes: set[str], second_likes: set[str]) -> float:
    if not first_likes or not second_likes:
        return 0.0

    similarity = len(first_likes & second_likes) / sqrt(
        len(first_likes) * len(second_likes)
    )
    return round(float(similarity) * 100, 2)


@router.get("/")
def get_matchmaking_result(
    request: Request,
    user1: str = Query(min_length=1),
    user2: str = Query(min_length=1),
):
    users_collection = request.app.state.users
    first_user = users_collection.find_one({"username": user1})
    second_user = users_collection.find_one({"username": user2})

    if first_user is None:
        raise HTTPException(status_code=404, detail=f"Ο χρήστης '{user1}' δεν βρέθηκε.")
    if second_user is None:
        raise HTTPException(status_code=404, detail=f"Ο χρήστης '{user2}' δεν βρέθηκε.")

    first_likes = set(first_user.get("liked_restaurants", []))
    second_likes = set(second_user.get("liked_restaurants", []))
    shared_ids = first_likes & second_likes
    percentage = cosine_match_percentage(first_likes, second_likes)

    object_ids = [ObjectId(restaurant_id) for restaurant_id in shared_ids if ObjectId.is_valid(restaurant_id)]
    restaurants = request.app.state.restaurants.find(
        {"_id": {"$in": object_ids}},
        {"name": 1, "cuisine": 1, "borough": 1},
    )
    common_restaurants = [
        {
            "id": str(restaurant["_id"]),
            "name": restaurant.get("name"),
            "cuisine": restaurant.get("cuisine"),
            "borough": restaurant.get("borough"),
        }
        for restaurant in restaurants
    ]

    return {
        "users": [first_user["username"], second_user["username"]],
        "match_percentage": percentage,
        "common_restaurants_count": len(common_restaurants),
        "common_restaurants": common_restaurants,
    }