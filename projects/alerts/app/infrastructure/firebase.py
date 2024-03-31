import firebase_admin
from firebase_admin import credentials, messaging


class FirebaseClient:
    def __init__(self, service_account_key_path: str):
        cred = credentials.Certificate(service_account_key_path)
        firebase_admin.initialize_app(cred)

    def send_fcm_alert(self, device_registration_token: list, priority: str, title: str, message: str):
        if device_registration_token is None or len(device_registration_token) == 0:
            return
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message,
            ),
            tokens=device_registration_token,
            android=messaging.AndroidConfig(priority=priority),
        )

        messaging.send_each_for_multicast(message)
