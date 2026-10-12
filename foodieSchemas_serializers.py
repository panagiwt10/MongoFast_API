from typing import Any, Mapping

def individual_data(restaurant: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(restaurant)
    data["id"] = str(data.pop("_id"))
    return data

def list_data(restaurants: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [individual_data(r) for r in restaurants]
