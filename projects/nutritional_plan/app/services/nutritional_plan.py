import json

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..models.schemas.schema import CaloricIntakeMessage, CaloricIntake
from ..config.db import get_db
from ..config.settings import Config
from ..infrastructure.aws import AWSClient


class NutritionalPlanService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.notification_queue = Config.NOTIFICATION_SQS_QUEUE

    def notify_caloric_intake(self, user_id: UUID4, caloric_intake: CaloricIntake):
        sqs = AWSClient().sqs
        sqs.send_message(self.notification_queue, json.dumps(
            CaloricIntakeMessage(user_id=user_id,
                                 message=f'You have {caloric_intake.calories} left to consume').__dict__
        ))
