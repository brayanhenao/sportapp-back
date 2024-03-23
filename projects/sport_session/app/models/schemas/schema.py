from pydantic import BaseModel, UUID4

from ..model import Sport


class SportSessionStart(BaseModel):
    user_id: UUID4
    sport: Sport
    latitude: float
    longitude: float


class SportSessionLocationUpdate(BaseModel):
    latitude: float
    longitude: float


class SportSessionLocation:
    user_id: UUID4
    latitude: float
    longitude: float

    def __init__(self, user_id: UUID4, latitude: float, longitude: float):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "latitude": self.latitude,
            "longitude": self.longitude
        }