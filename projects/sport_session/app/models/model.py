import enum
from uuid import uuid4

from sqlalchemy import Column, DateTime, Uuid, Boolean, Float, Enum
from ..config.db import Base


class Sport(enum.Enum):
    RUNNING = 'running'
    CYCLING = 'cycling'
    SWIMMING = 'swimming'
    WALKING = 'walking'


class SportSession(Base):
    __tablename__ = 'sport_session'
    sport_session_id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(Uuid(as_uuid=True), nullable=False)
    sport = Column(Enum(Sport), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    calories = Column(Float)
    active = Column(Boolean, nullable=False, default=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
