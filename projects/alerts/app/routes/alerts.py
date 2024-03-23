from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..config.db import get_db
from ..models.schemas.schema import UserAlertDeviceCreate
from ..services.alerts import AlertService

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register-device")
async def register_device(user_device: UserAlertDeviceCreate, db: Session = Depends(get_db)):
    alert_service = AlertService(db)
    alert_created = alert_service.register_device(user_device)
    return JSONResponse(
        {
            "user_id": str(alert_created.user_id),
            "device_token": alert_created.device_token,
            "enabled": alert_created.enabled
        },
        status_code=201
    )


@router.delete("/{user_id}/remove-device")
async def remove_user_device(user_id: str, device_token: str, db: Session = Depends(get_db)):
    alert_service = AlertService(db)
    removed = alert_service.remove_user_device(user_id, device_token)
    return JSONResponse(
        {
            "removed": removed
        },
        status_code=200
    )


@router.put("/{user_id}/disable-device")
async def disable_user_device(user_id: str, device_token: str, db: Session = Depends(get_db)):
    alert_service = AlertService(db)
    disabled = alert_service.disable_user_device(user_id, device_token)
    return JSONResponse(
        {
            "disabled": disabled
        },
        status_code=200
    )


@router.get("/{user_id}/devices")
async def get_user_devices(user_id: str, db: Session = Depends(get_db)):
    alert_service = AlertService(db)
    devices = alert_service.get_user_devices(user_id)
    return JSONResponse(
        {
            "devices": devices
        },
        status_code=200
    )
