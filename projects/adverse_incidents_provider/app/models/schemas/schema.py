class BoundingBox:
    latitude_from: float
    longitude_from: float
    latitude_to: float
    longitude_to: float

    def __init__(self, latitude_from: float, longitude_from: float, latitude_to: float, longitude_to: float):
        self.latitude_from = latitude_from
        self.longitude_from = longitude_from
        self.latitude_to = latitude_to
        self.longitude_to = longitude_to

    def to_dict(self):
        return {
            "latitude_from": self.latitude_from,
            "longitude_from": self.longitude_from,
            "latitude_to": self.latitude_to,
            "longitude_to": self.longitude_to,
        }


class AdverseIncident:
    description: str
    bounding_box: BoundingBox

    def __init__(self, description: str, bounding_box: BoundingBox):
        self.description = description
        self.bounding_box = bounding_box

    def to_dict(self):
        return {"description": self.description, "bounding_box": self.bounding_box.to_dict()}
