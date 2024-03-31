from datetime import datetime

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..config.db import get_db
from ..models.model import SportSession
from ..models.schemas.schema import SportSessionStart, SportSessionLocationUpdate, SportSessionLocation
from ..exceptions.exceptions import NotFoundError


class SportSessionService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def start_sport_session(self, sport_session_data: SportSessionStart):
        sport_session = SportSession(
            user_id=sport_session_data.user_id,
            sport=sport_session_data.sport,
            start_time=datetime.now(),
            active=True,
            latitude=sport_session_data.latitude,
            longitude=sport_session_data.longitude,
        )
        self.db.add(sport_session)
        self.db.commit()
        self.db.refresh(sport_session)

        return_sport_session = {
            "sport_session_id": str(sport_session.sport_session_id),
            "user_id": str(sport_session.user_id),
            "sport": sport_session.sport.value,
            "start_time": sport_session.start_time.isoformat(),
            "active": sport_session.active,
            "latitude": sport_session.latitude,
            "longitude": sport_session.longitude,
        }

        return return_sport_session

    def finish_sport_session(self, sport_session_id: UUID4, calories: float):
        sport_session = self.db.query(SportSession).filter(SportSession.sport_session_id == sport_session_id).filter(SportSession.active).first()
        if not sport_session:
            raise NotFoundError(f"Sport session {sport_session_id} not found")
        sport_session.active = False
        sport_session.end_time = datetime.now()
        sport_session.calories = calories
        self.db.commit()
        self.db.refresh(sport_session)

        return_sport_session = {
            "sport_session_id": str(sport_session.sport_session_id),
            "user_id": str(sport_session.user_id),
            "sport": sport_session.sport.value,
            "start_time": sport_session.start_time.isoformat(),
            "end_time": sport_session.end_time.isoformat(),
            "calories": sport_session.calories,
            "active": sport_session.active,
            "latitude": sport_session.latitude,
            "longitude": sport_session.longitude,
        }

        return return_sport_session

    def update_sport_session_location(self, sport_session_id: UUID4, location_data: SportSessionLocationUpdate):
        sport_session = self.db.query(SportSession).filter(SportSession.sport_session_id == sport_session_id).filter(SportSession.active).first()
        if not sport_session:
            raise NotFoundError(f"Sport session {sport_session_id} not found")
        sport_session.latitude = location_data.latitude
        sport_session.longitude = location_data.longitude
        self.db.commit()
        self.db.refresh(sport_session)

        return_sport_session = {
            "sport_session_id": str(sport_session.sport_session_id),
            "user_id": str(sport_session.user_id),
            "sport": sport_session.sport.value,
            "start_time": sport_session.start_time.isoformat(),
            "active": sport_session.active,
            "latitude": sport_session.latitude,
            "longitude": sport_session.longitude,
        }

        return return_sport_session

    def get_active_users_locations(self):
        sport_sessions = self.db.query(SportSession).filter(SportSession.active).all()
        users_locations = []
        for sport_session in sport_sessions:
            sport_session_location = SportSessionLocation(sport_session.user_id, sport_session.latitude, sport_session.longitude)
            users_locations.append(sport_session_location)

        return [sport_session_location.to_dict() for sport_session_location in users_locations]

    def get_sport_sessions(self):
        sport_sessions = self.db.query(SportSession).all()
        return [
            {
                "sport_session_id": str(sport_session.sport_session_id),
                "user_id": str(sport_session.user_id),
                "sport": sport_session.sport.value,
                "start_time": sport_session.start_time.isoformat(),
                "end_time": sport_session.end_time.isoformat() if sport_session.end_time else None,
                "calories": sport_session.calories,
                "active": sport_session.active,
                "latitude": sport_session.latitude,
                "longitude": sport_session.longitude,
            }
            for sport_session in sport_sessions
        ]
