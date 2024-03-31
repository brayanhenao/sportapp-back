import os


class Config:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    NOTIFICATION_SQS_QUEUE = os.getenv("NOTIFICATION_SQS_QUEUE", "nutritional_plan_queue.fifo")
