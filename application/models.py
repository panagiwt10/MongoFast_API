from typing import Any

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    preferences: dict[str, Any]