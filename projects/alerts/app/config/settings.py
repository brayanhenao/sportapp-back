import os


class Config:
    ADVERSE_INCIDENTS_ALERTS_QUEUE = os.environ.get('ADVERSE_INCIDENTS_ALERTS_QUEUE', 'adverse_incidents_queue.fifo')
    NUTRITIONAL_PLAN_ALERTS_QUEUE = os.environ.get('NUTRITIONAL_PLAN_ALERTS_QUEUE', 'nutritional_plan_queue.fifo')
