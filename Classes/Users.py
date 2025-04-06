from Utils.Response import ApiResponse
from Models.UsersModel import UsersModel
from Utils.Tools.TypingTools import EventType
from Helpers.GeneralTools import (
    get_input_data, hash_password, validate_password
)
from Utils.Tools.ValidationTools import validate_field
from Utils.Constants.Constant import COGNITO_IDP
import Schemas.UserSchemas as UserSchemas
from Helpers.ProcessSql import ProcessSql
from Helpers.BasicHelper import BasicHelper
from http import HTTPStatus
from typing import TypedDict
import boto3
import os

class RequestsUsers(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str

class Users:
    
    def __init__(self):
        self.__region = os.environ.get("REGION")
        self.__user_pool = os.environ.get("USER_POOL")
        self.cognito_client = boto3.client(
            COGNITO_IDP,
            region_name=self.__region
        )
        self.schemas = UserSchemas
        self.process_sql = ProcessSql()
        self.basic_helper = BasicHelper()
    
    def create_user(self, event: EventType) -> ApiResponse:
        """
        Handles the creation of a new user.

        Args:
            event (EventType): The event object containing request data which contains 
                the fields to create the new user data.

        Returns:
            ApiResponse: The response object containing the status code and user data.
        """
        request: RequestsUsers = get_input_data(event)

        validate_field(self.schemas.CreateUserSchema(), request)
        validate_password(request['password'])

        self.basic_helper.validate_if_field_exists(
            UsersModel, 
            {'email': request['email']},
            value= "email"
        )
        password_without_hash = request['password']
        request['password'] = hash_password(request['password'])

        new_user = self.process_sql.insert(
            model=UsersModel(**request),
        )

        self.create_user_cognito({
            "email": request['email'],  
            "password": password_without_hash
        })

        return ApiResponse(
            status_code=HTTPStatus.CREATED,
            data={
                "user_id": new_user,
                **request
            }
        )

    def create_user_cognito(self, request: RequestsUsers) -> bool:
        """
        Creates a new user in Amazon Cognito and sets their password as permanent.

        The process involves two steps:
        1. Creating the user with a temporary password.
        2. Immediately setting the password as permanent to avoid requiring a password reset on first login.

        Args:
            request (RequestsUsers): A dictionary-like object containing at least the user's 'email' and 'password'.

        Returns:
            dict: The response from the `admin_set_user_password` call indicating the result of setting the password.

        Raises:
            botocore.exceptions.ClientError: If any Cognito operation fails.
            """
        email = request['email']
        password = request['password']

        # Create the user in Cognito
        self.cognito_client.admin_create_user(
            UserPoolId=self.__user_pool,
            Username=email, 
            TemporaryPassword=password,
            UserAttributes=[
                {'Name': 'email', 'Value': request['email']},
                {'Name': 'email_verified', 'Value': 'true'},
            ],
            DesiredDeliveryMediums=['EMAIL'],
            ForceAliasCreation=False
        )

        # Set the password for the user in Cognito
        self.cognito_client.admin_set_user_password(
            UserPoolId=self.__user_pool,
            Username=email,
            Password=password,
            Permanent=True
        )
        '''
        Permanent=True -> Esto establece la contraseña como permanente,
        en lugar de requerir un cambio en el próximo inicio de sesión
        '''
        return True
