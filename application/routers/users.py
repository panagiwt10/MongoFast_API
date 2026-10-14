from fastapi import APIRouter, HTTPException, Request

from models import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users & Preferences"]
)

@router.post("/", status_code=201)
def create_or_update_user(
    request: Request,
    user_data: UserCreate
):
    users_collection = request.app.state.users

    result = users_collection.update_one(
        {"username": user_data.username},
        {
            "$set": {
                "preferences": user_data.preferences,
            },
            "$setOnInsert": {
                "liked_restaurants": []
            }
        },
        upsert=True
    )

    return {
        "status": "success",
        "username": user_data.username,
        "message": f"Ο χρήστης {user_data.username} αποθηκεύτηκε επιτυχώς!"
    }


@router.post("/seed-random-likes")
def seed_random_likes(request: Request):
    restaurants_collection = request.app.state.restaurants
    users_collection = request.app.state.users
    sample_restaurants = list(
        restaurants_collection.aggregate([{"$sample": {"size": 4}}])
    )

    if len(sample_restaurants) < 4:
        raise HTTPException(
            status_code=400,
            detail="Χρειάζονται τουλάχιστον 4 εστιατόρια για το seed."
        )

    restaurant_ids = [str(restaurant["_id"]) for restaurant in sample_restaurants]
    shared_ids = restaurant_ids[:2]
    nikos_ids = shared_ids + [restaurant_ids[2]]
    maria_ids = shared_ids + [restaurant_ids[3]]

    seeded_users = {
        "nikos": {
            "preferences": {"cuisine": "Italian", "borough": "Manhattan"},
            "liked_restaurants": nikos_ids,
        },
        "panos": {
            "preferences": {"cuisine": "Italian", "borough": "Brooklyn"},
            "liked_restaurants": maria_ids,
        },
    }

    for username, data in seeded_users.items():
        users_collection.update_one(
            {"username": username},
            {
                "$set": {"liked_restaurants": data["liked_restaurants"]},
                "$setOnInsert": {"preferences": data["preferences"]},
            },
            upsert=True,
        )

    return {
        "message": "Τα τυχαία likes μοιράστηκαν επιτυχώς.",
        "nikos_liked_restaurants": nikos_ids,
        "maria_liked_restaurants": maria_ids,
        "shared_restaurants": shared_ids,
    }

