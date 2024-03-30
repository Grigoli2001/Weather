from pydantic import BaseModel
from typing import  Optional

class LocationBase(BaseModel):
    id: Optional[int] = None
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    weather: Optional[dict] = None

    class config:
        orm_mode = True

class LocationCreate(BaseModel):
    name: str