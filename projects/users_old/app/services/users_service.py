from fastapi import Depends
from sqlalchemy.orm import Session

from ..config.db import get_db
from ..infrastructure.aws import AWSClient
from ..models.mappers.mapper import DataClassMapper
from ..models.model import User
from ..models.schemas.schema import UserCreate, UserCredentials


class UsersService:
    def __init__(self, db: Session = Depends(get_db)):
        self.aws_client = AWSClient()
        self.db = db
        self.mapper = DataClassMapper(User)

    def register_user(self, user: UserCreate):
        cognito_user_created = self.aws_client.cognito.create_user(user=user)

        self.aws_client.cognito.set_permanent_password(sub=cognito_user_created["User"]["Username"], password=user.password)

        user_created = User()
        user_created.email = user.email
        user_created.first_name = user.first_name
        user_created.last_name = user.last_name

        self.db.add(user_created)
        self.db.commit()
        self.db.refresh(user_created)

        return self.mapper.to_dict(user_created)

    def login_user(self, user_login: UserCredentials):
        response = self.aws_client.cognito.get_user_token(refresh_token=user_login.refresh_token, username=user_login.email, password=user_login.password)

        return response

    def get_user(self, user_id: str):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        return self.mapper.to_dict(user)

    def get_users(self):
        users = self.db.query(User).all()
        return [self.mapper.to_dict(user) for user in users]

    def delete_user(self, user_id: str):
        user = self.db.query(User).filter(User.user_id == user_id).first()
        self.db.delete(user)
        self.db.commit()
        return self.mapper.to_dict(user)

    def complete_user_registration(self, user_id: str): ...
