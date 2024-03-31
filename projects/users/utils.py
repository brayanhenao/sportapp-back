import boto3
from os import environ as env
from models import User


class AWSClient:
    def __init__(self):
        self.session = boto3.Session(
            region_name=env.get("AWS_REGION", "us-east-1"),
        )

        self.cognito = Cognito(self.session)


class Cognito:
    def __init__(self, session):
        USER_POOL_ID = env.get("USER_POOL_ID")
        CLIENT_ID = env.get("CLIENT_ID")

        self.client = session.client("cognito-idp")
        self.user_pool_id = USER_POOL_ID
        self.client_id = CLIENT_ID

    def create_user(self, user: User):
        response = self.client.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=user.email,
            MessageAction="SUPPRESS",
            UserAttributes=[
                {"Name": "email", "Value": user.email},
                {"Name": "email_verified", "Value": "True"},
                {"Name": "name", "Value": user.first_name},
                {"Name": "family_name", "Value": user.last_name},
                {"Name": "custom:user_id", "Value": str(user.user_id)},
            ],
        )

        return response

    def set_permanent_password(self, email: str, password: str):
        self.client.admin_set_user_password(UserPoolId=self.user_pool_id, Username=email, Password=password, Permanent=True)

    def refresh_token(self, refresh_token: str):
        response = self.client.initiate_auth(
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
            },
            ClientId=self.client_id,
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
            ClientId=self.client_id,
        )

        login_response = {
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "refresh_token": response["AuthenticationResult"]["RefreshToken"],
        }

        return login_response

    def delete_user(self, username: str):
        self.client.admin_delete_user(UserPoolId=self.user_pool_id, Username=username)
