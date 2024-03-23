import os

import boto3

from ..config.settings import Config


class SQS:
    def __init__(self, session: boto3.Session):
        self.sqs = session.client("sqs")

    def send_message(self, queue_name: str, message: str):
        self.sqs.send_message(QueueUrl=queue_name, MessageBody=message, MessageGroupId="nutritional_plan")
        print(f"Message sent {message}")

    def get_messages(self, queue_name: str):
        messages = self.sqs.receive_messages(QueueUrl=queue_name)
        return messages

    def delete_message(self, queue_name: str, message):
        self.sqs.delete_messages(QueueUrl=queue_name,
                                 Entries=[{"Id": message.message_id, "ReceiptHandle": message.receipt_handle}])
        print(f"Message deleted {message.body}")


class AWSClient:
    def __init__(self):
        self.session = boto3.Session(
            region_name=Config.AWS_REGION
        )

        self.sqs = SQS(self.session)
