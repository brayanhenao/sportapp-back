import os

import boto3


class SQS:
    def __init__(self, session: boto3.Session):
        self.sqs = session.client("sqs")

    def send_message(self, queue_name: str, message: str):
        queue = self.sqs.send_message(QueueUrl=queue_name, MessageBody=message, MessageGroupId="1")
        print(f"Message sent to {queue}: {message}")

    def get_messages(self, queue_name: str):
        messages = self.sqs.receive_message(QueueUrl=queue_name)
        return messages

    def delete_message(self, queue_name: str, message):
        self.sqs.delete_message(QueueUrl=queue_name, ReceiptHandle=message["ReceiptHandle"])
        print(f"Message deleted from {queue_name}")


class AWSClient:
    def __init__(self):
        self.session = boto3.Session(
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        self.sqs = SQS(self.session)
