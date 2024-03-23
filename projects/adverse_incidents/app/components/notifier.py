import time

import requests

from ..config.settings import Config
from ..services.adverse_incidents import AdverseIncidentsService

# Global flag to signal the thread to stop
stop_thread = False


def get_incidents():
    adverse_incidents_service = AdverseIncidentsService()
    while not stop_thread:
        try:
            response = requests.get(Config.ADVERSE_INCIDENTS_PROVIDER_URL,
                                    headers={"x-api-key": Config.ADVERSE_INCIDENTS_PROVIDER_API_KEY})
            if response.status_code == 200:
                incidents = response.json()
                adverse_incidents_service.process_adverse_incidents(incidents["incidents"])
            else:
                print(f"HTTPError: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(
                f"Waiting {Config.ADVERSE_INCIDENTS_PROVIDER_REFRESH_INTERVAL_SECONDS} seconds to get the next "
                f"incidents...")
            time.sleep(Config.ADVERSE_INCIDENTS_PROVIDER_REFRESH_INTERVAL_SECONDS)


def stop_processing():
    global stop_thread
    stop_thread = True
