import json
from time import sleep

from ..config.settings import Config
from . import publisher
from ..infrastructure.aws import AWSClient

sqs = AWSClient().sqs

nutritional_plan_queue_name = Config.NUTRITIONAL_PLAN_ALERTS_QUEUE
adverse_incidents_queue_name = Config.ADVERSE_INCIDENTS_ALERTS_QUEUE

# Global flag to signal the thread to stop
stop_thread = False


def process_queues():
    while not stop_thread:
        nutritional_plan_messages = sqs.get_messages(nutritional_plan_queue_name)
        if nutritional_plan_messages:
            for message in nutritional_plan_messages.get("Messages", []):
                body = json.loads(message["Body"])
                print(f"Received nutritional plan message: {body}")
                publisher.send_alert(body["user_id"], "high", "Nutritional Plan", body["message"])
                sqs.delete_message(nutritional_plan_queue_name, message)
        adverse_incidents_queue = sqs.get_messages(adverse_incidents_queue_name)
        if adverse_incidents_queue:
            for message in adverse_incidents_queue.get("Messages", []):
                body = json.loads(message["Body"])
                print(f"Received adverse incident message: {body}")
                publisher.send_alert(body["user_id"], "high", "Adverse Incident", body["message"])
                sqs.delete_message(adverse_incidents_queue_name, message)
        sleep(0.5)


def stop_processing():
    global stop_thread
    stop_thread = True
