from pydantic import BaseModel, UUID4
from typing import Optional


class UserAlertDeviceCreate(BaseModel):
    user_id: UUID4
    device_token: str
    enabled: Optional[bool] = True
