import enum
from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column, Uuid, Enum, String, Integer, Float, Boolean
from ..config.db import Base


class UserIdentificationType(enum.Enum):
    CEDULA_CIUDADANIA = "CC"
    CEDULA_EXTRANJERIA = "CE"
    PASAPORTE = "PA"
    TARJETA_IDENTIDAD = "TI"


class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    PREFER_NOT_TO_SAY = "P"


class TrainingLimitation(Base):
    __tablename__ = "training_limitations"
    limitation_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class NutritionLimitation(Base):
    __tablename__ = "nutrition_limitations"
    limitation_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class UserNutritionLimitation(Base):
    __tablename__ = "user_nutrition_limitations"
    user_id = Column(Uuid(as_uuid=True), primary_key=True)
    limitation_id = Column(Uuid(as_uuid=True), primary_key=True)


class UserTrainingLimitation(Base):
    __tablename__ = "user_training_limitations"
    user_id = Column(Uuid(as_uuid=True), primary_key=True)
    limitation_id = Column(Uuid(as_uuid=True), primary_key=True)


class UserSport(Base):
    __tablename__ = "user_sport"
    user_id = Column(Uuid(as_uuid=True), primary_key=True)
    sport_id = Column(Uuid(as_uuid=True), primary_key=True)


class FoodPreference(enum.Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    EVERYTHING = "everything"


class UserSubscriptionType(enum.Enum):
    FREE = "free"
    INTERMEDIATE = "intermediate"
    PREMIUM = "premium"


@dataclass
class User(Base):
    __tablename__ = "users"
    # Basic info
    user_id: str = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    # Additional info
    identification_type: str = Column(Enum(UserIdentificationType))
    identification_number: str = Column(String)
    gender: str = Column(Enum(Gender))
    country_of_birth: str = Column(String)
    city_of_birth: str = Column(String)
    country_of_residence: str = Column(String)
    city_of_residence: str = Column(String)
    residence_age: int = Column(Integer)
    # Demographic profile
    age: int = Column(Integer)
    weight: float = Column(Float)
    height: float = Column(Float)
    bmi: float = Column(Float)
    # Sport profile
    training_years: int = Column(Integer)
    training_hours_per_week: int = Column(Integer)
    available_training_hours_per_week: int = Column(Integer)
    food_preference: str = Column(Enum(FoodPreference))
    # Subscription info
    subscription_type: str = Column(Enum(UserSubscriptionType))
