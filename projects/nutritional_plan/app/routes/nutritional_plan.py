import math
import random

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from ..models.schemas.schema import CaloricIntake
from ..services.nutritional_plan import NutritionalPlanService

router = APIRouter(
    prefix="/nutritional-plan",
    tags=["nutritional-plan"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{user_id}/notify-caloric-intake")
async def notify_caloric_intake(user_id: str, caloric_intake: CaloricIntake,
                                alert_service: NutritionalPlanService = Depends()):
    alert_service.notify_caloric_intake(user_id, caloric_intake)
    return JSONResponse(status_code=200, content={"message": "Notification sent successfully"})
