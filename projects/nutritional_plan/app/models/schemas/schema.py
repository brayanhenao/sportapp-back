from pydantic import BaseModel


class CaloricIntakeMessage:
    user_id: str
    message: str

    def __init__(self, user_id: str, message: str):
        self.user_id = user_id
        self.message = message


class CaloricIntake(BaseModel):
    calories: float
