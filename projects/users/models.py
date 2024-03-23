import uuid

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Uuid
from db import Base


class User(Base):
    __tablename__ = "mock"
    user_id: str = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
