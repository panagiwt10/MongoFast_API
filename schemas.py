from collections.abc import Iterable, Mapping
from typing import Any


def individual_data(restaurant: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(restaurant)
    data["id"] = str(data.pop("_id"))
    return data


def list_data(restaurants: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [individual_data(restaurant) for restaurant in restaurants]