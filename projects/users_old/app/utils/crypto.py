import base64
import hashlib
import hmac


def generate_cognito_secret_hash(client_id: str, client_secret: str, username: str):
    key = bytes(client_secret, "latin-1")
    msg = bytes(username + client_id, "latin-1")
    new_digest = hmac.new(key, msg, hashlib.sha256).digest()
    return base64.b64encode(new_digest).decode()
