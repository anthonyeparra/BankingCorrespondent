from Utils.Response import ApiResponse
from Utils.Tools.TypingTools import EventType
from Helpers.GeneralTools import get_input_data
from Utils.Tools.ValidationTools import validate_field
from Utils.Constants.Constant import COGNITO_IDP
import Schemas.AuthSchemas as AuthSchemas
from Helpers.ProcessSql import ProcessSql
from Helpers.BasicHelper import BasicHelper
from http import HTTPStatus
import boto3
import os
import hmac
import hashlib
import base64

class Authentication:  
    def __init__(self):
        self.__region = os.environ.get("REGION")
        self.__user_pool_client = os.environ.get("USER_POOL_CLIENT")
        self.__client_secret = os.environ.get("CLIENT_SECRET")
        self.cognito_client = boto3.client(
            COGNITO_IDP,
            region_name=self.__region
        )
        self.schemas = AuthSchemas
        self.process_sql = ProcessSql()
        self.basic_helper = BasicHelper()

    def login(self, event: EventType) -> ApiResponse:
        """
        Authenticates a user using Amazon Cognito and returns authentication tokens.

        This method extracts the user's email and password from the provided event,
        generates the necessary secret hash, and initiates the authentication flow
        using Cognito's USER_PASSWORD_AUTH. It then retrieves and returns the authentication
        tokens in an ApiResponse object.

        Args:
            event (EventType): The event containing the input data, including the user's
                            email and password.

        Returns:
            ApiResponse: An object containing the HTTP status code and the authentication tokens
                        (AccessToken, Idtoken, and optionally RefreshToken).
        """
        request = get_input_data(event)

        validate_field(self.schemas.GetAuth(), request)

        email = request['email']
        flow_type = "USER_PASSWORD_AUTH"
        
        auth_params = {
            "USERNAME": email,
            "PASSWORD": request['password'],
            "SECRET_HASH": self.__get_secret_hash(email)
        }
        tokens = self.get_tokens(flow_type, auth_params)

        return ApiResponse(
            status_code=HTTPStatus.OK,
            data=tokens
        )
        
    
    def get_tokens(self, auth_flow: str, auth_params: dict):
        """
        Initiates an authentication flow with Amazon Cognito and retrieves authentication tokens.

        This method calls the Cognito client's `initiate_auth` function using the provided 
        authentication flow and parameters. It then extracts the tokens from the authentication 
        result. For the USER_PASSWORD_AUTH flow, it also includes the refresh token.

        Args:
            auth_flow (str): The authentication flow to use (e.g., "USER_PASSWORD_AUTH").
            auth_params (dict): A dictionary of authentication parameters such as USERNAME, 
                PASSWORD, and optionally SECRET_HASH.

        Returns:
            dict: A dictionary containing the following keys:
                - "AccessToken": The access token for authenticated requests.
                - "Idtoken": The ID token containing user identity information.
                - "RefreshToken" (optional): The refresh token, present if the flow is 
                USER_PASSWORD_AUTH.
        """
        response = self.cognito_client.initiate_auth(
            ClientId=self.__user_pool_client,
            AuthFlow=auth_flow,
            AuthParameters=auth_params
        )
        tokens_result = response["AuthenticationResult"]
        tokens = {}
        tokens["AccessToken"] = tokens_result["AccessToken"]
        tokens["Idtoken"] = tokens_result["IdToken"]
        if auth_flow == "USER_PASSWORD_AUTH":
            tokens["RefreshToken"] = tokens_result["RefreshToken"]
        return tokens
    
    
    def __get_secret_hash(self, username: str) -> str:
        """
        Generates a secret hash for AWS Cognito authentication.

        This method computes an HMAC-SHA256 hash using the concatenation of the username
        and the user pool client ID, with the client secret as the key. The resulting digest
        is then base64-encoded and returned as a string. This hash is required when the 
        Cognito App Client is configured with a client secret.

        Args:
            username (str): The username for which the secret hash will be generated.

        Returns:
            str: The base64-encoded secret hash used for authentication.
        """
        message = username + self.__user_pool_client
        dig = hmac.new(
            self.__client_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()