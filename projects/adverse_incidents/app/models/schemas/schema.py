class AdverseIncidentMessage:
    user_id: str
    message: str

    def __init__(self, user_id: str, message: str):
        self.user_id = user_id
        self.message = message


class AdverseIncident:
    description: str
    latitude_from: float
    longitude_from: float
    latitude_to: float
    longitude_to: float

    def __init__(self, description: str, latitude_from: float, longitude_from: float, latitude_to: float, longitude_to: float):
        self.description = description
        self.latitude_from = latitude_from
        self.longitude_from = longitude_from
        self.latitude_to = latitude_to
        self.longitude_to = longitude_to
