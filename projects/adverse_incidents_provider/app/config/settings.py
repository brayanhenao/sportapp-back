import os


class Config:
    ADVERSE_INCIDENTS_AFFECTED_RANGE = os.environ.get('ADVERSE_INCIDENTS_AFFECTED_RANGE', 0.5)
