import os

from ..config.db import get_db
from ..infrastructure.firebase import FirebaseClient
from ..services.alerts import AlertService

firebase_client = FirebaseClient("serviceAccountKey.json")


def send_alert(user_id: str, priority: str, title: str, message: str):
    alerts_service = AlertService(get_db())
    user_devices = alerts_service.get_user_devices(user_id)
    firebase_client.send_fcm_alert(user_devices, priority, title, message)
