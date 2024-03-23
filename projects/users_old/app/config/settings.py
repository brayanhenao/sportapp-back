import os


class Config:
    USER_POOL_ID = os.environ.get("USER_POOL_ID")
    CLIENT_ID = os.environ.get("CLIENT_ID")
