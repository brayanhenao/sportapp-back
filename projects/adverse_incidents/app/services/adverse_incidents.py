import json
import time
import requests

from ..config.settings import Config
from ..models.schemas.schema import AdverseIncidentMessage, AdverseIncident
from ..infrastructure.aws import AWSClient


class AdverseIncidentsService:
    def __init__(self):
        self.notification_queue = Config.NOTIFICATION_SQS_QUEUE

    def _notify_adverse_incident(self, message: AdverseIncidentMessage):
        sqs_client = AWSClient().sqs
        timestamp = time.time_ns() // 1_000_000
        print(f"Adverse incident notification sent at {timestamp} ms")
        sqs_client.send_message(self.notification_queue, json.dumps(message.__dict__))

    def _get_users_affected_by_incident(self, incident: AdverseIncident):
        try:
            user_locations = requests.get(f"{Config.SPORT_SESSION_URL}/active-sessions").json()
        except Exception as e:
            print(f"Error: {e}")
            return []
        users_affected = []
        for user in user_locations:
            if incident.latitude_from <= user["latitude"] <= incident.latitude_to and incident.longitude_from <= user["longitude"] <= incident.longitude_to:
                users_affected.append(user["user_id"])
        return users_affected

    def _process_adverse_incident(self, incident: AdverseIncident):
        users_affected = self._get_users_affected_by_incident(incident)
        for user_id in users_affected:
            self._notify_adverse_incident(AdverseIncidentMessage(user_id=user_id, message=incident.description))

    def process_adverse_incidents(self, incidents: list):
        for incident in incidents:
            self._process_adverse_incident(
                AdverseIncident(
                    description=incident["description"],
                    latitude_from=incident["bounding_box"]["latitude_from"],
                    longitude_from=incident["bounding_box"]["longitude_from"],
                    latitude_to=incident["bounding_box"]["latitude_to"],
                    longitude_to=incident["bounding_box"]["longitude_to"],
                ),
            )
