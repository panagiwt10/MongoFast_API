from datetime import datetime
from pydantic import BaseModel


class Address(BaseModel):
    building: str
    coord: list[float]
    street: str
    zipcode: str


class Grade(BaseModel):
    date: datetime
    grade: str
    score: int


class RestaurantCreate(BaseModel):
    name: str
    borough: str
    cuisine: str
    address: Address
    grades: list[Grade]


class Restau(RestaurantCreate):
    id: str