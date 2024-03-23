import enum

from sqlalchemy import Column, String, DateTime, Enum, Uuid, func, Boolean, UniqueConstraint

from ..config.db import Base


class UserAlertDevice(Base):
    __tablename__ = 'user_alert_devices'

    user_id = Column(Uuid(as_uuid=True), primary_key=True, nullable=False)
    device_token = Column(String, primary_key=True, nullable=False)
    enabled = Column(Boolean, default=True)
