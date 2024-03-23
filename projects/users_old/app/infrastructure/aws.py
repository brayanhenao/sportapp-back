import json
import os

import boto3

from ..config.settings import Config
from ..models.schemas.schema import UserCreate
from ..utils.crypto import generate_cognito_secret_hash


class Cognito:
    def __init__(self, session):
        self.client = session.client("cognito-idp")
        self.user_pool_id = Config.USER_POOL_ID
        self.client_id = Config.CLIENT_ID

    def create_user(self, user: UserCreate):
        response = self.client.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=user.email,
            MessageAction="SUPPRESS",
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": user.email
                },
                {
                    "Name": "email_verified",
                    "Value": "True"
                },
                {
                    "Name": "name",
                    "Value": user.first_name
                },
                {
                    "Name": "family_name",
                    "Value": user.last_name
                }
            ]
        )

        return response

    def set_permanent_password(self, sub: str, password: str):
        self.client.admin_set_user_password(
            UserPoolId=self.user_pool_id,
            Username=sub,
            Password=password,
            Permanent=True
        )

    def refresh_token(self, refresh_token: str):
        response = self.client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
            },
            ClientId=self.client_id
        )

        login_response = {
            "access_token": response["AuthenticationResult"]["AccessToken"],
        }

        return login_response

    def get_user_token(self, refresh_token: str, username: str, password: str):
        if refresh_token is not None:
            return self.refresh_token(refresh_token)

        response = self.client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
            },
            ClientId=self.client_id
        )

        login_response = {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"]
        }

        return login_response


class AWSClient:
    def __init__(self):
        self.session = boto3.Session(
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        self.cognito = Cognito(self.session)
