from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..config.db import get_db
from ..exceptions.exceptions import NotFoundError
from ..models.model import UserAlertDevice
from ..models.schemas.schema import UserAlertDeviceCreate


class AlertService:
    def __init__(self, db: Session):
        # check if db is a session. If not it is a generator
        if isinstance(db, Session):
            self.db = db
        else:
            self.db = next(db)

    def register_device(self, alert_data: UserAlertDeviceCreate):
        alert = UserAlertDevice(
            user_id=alert_data.user_id,
            device_token=alert_data.device_token,
            enabled=alert_data.enabled
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def remove_user_device(self, user_id: UUID4, device_token: str):
        device = self.db.query(UserAlertDevice).filter(UserAlertDevice.user_id == user_id).filter(
            UserAlertDevice.device_token == device_token).first()
        if not device:
            raise NotFoundError(f"Device {device_token} not found for user {user_id}")

        self.db.delete(device)
        self.db.commit()
        return True

    def disable_user_device(self, user_id: UUID4, device_token: str):
        device = self.db.query(UserAlertDevice).filter(UserAlertDevice.user_id == user_id).filter(
            UserAlertDevice.device_token == device_token).first()
        if not device:
            raise NotFoundError(f"Device {device_token} not found for user {user_id}")
        device.enabled = False
        self.db.commit()
        return True

    def get_user_devices(self, user_id: UUID4):
        devices = self.db.query(UserAlertDevice).filter(UserAlertDevice.user_id == user_id).all()
        return [str(device.device_token) for device in devices]
