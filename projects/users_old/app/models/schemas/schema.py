from typing import Optional

from pydantic import BaseModel, model_validator


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserCredentials(BaseModel):
    refresh_token: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    @model_validator(mode='before')
    def validate_credentials(cls, values):
        refresh_token = values.get("refresh_token")
        email = values.get("email")
        password = values.get("password")

        if refresh_token is not None:
            if any((email, password)):
                raise ValueError("Cannot provide refresh_token along with email and password")
        elif all((email, password)):
            return values
        else:
            raise ValueError("Either provide refresh_token or both email and password")

        return values
