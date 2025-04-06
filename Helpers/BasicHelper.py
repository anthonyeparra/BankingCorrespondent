from Utils.CustomException import CustomException
from Helpers.ProcessSql import ProcessSql
from Utils.Constants.ErrorMessages import (
    VALUE_ALREADY_EXISTS,
    VALUE_NOT_EXISTS
)
from typing import Union
from Utils.Tools.QueryTools import get_primary_key


class BasicHelper:
    def __init__(self):
        self.process_sql = ProcessSql()
        
    def validate_if_field_exists(
            self,
            model,
            request: dict,
            type_: str = 'create',
            id_: Union[int, None] = None,
            value: Union[int, None]=None
            ) -> None:
         
        """
        Validate the existence of a record in the database.

        Args:
            model (object): The model to validate the record in.
            request (dict): The data to validate. It should contain the field to validate.
            type_ (str): The type of validation. It can be 'create' or 'update'.
            id_ (int): The ID of the record to update. It is only used when type_ is 'update'.
            value (int): The value of the field to validate. If not provided, it will be the primary key of the model.

        Raises:
            CustomException: If the field already exists in the database.
        """
        
        get_data = {
            'model': model,
            'request': request,
            'like_filter': list(request.keys()),
            'columns': [get_primary_key(model)]
        }

        if type_ == 'update':
            request[get_primary_key(model)] = id_
            get_data['unequal_filter'] = [get_primary_key(model)]
        
        print("get_data", get_data)
        
        response = self.process_sql.get_data(
            **get_data
        )

        value = get_primary_key(model) if not value else value

        if response:
            raise CustomException(
                VALUE_ALREADY_EXISTS.format(value)
            )

    def validate_if_does_not_exist(
            self,
            model,
            request: dict,
            message: Union[str, None] = None
        ):
        
        """
        Validate that a record does not exist in the database.

        Args:
            model (object): The model to validate the record in.
            request (dict): The conditions to filter the records to retrieve.
            message (str): The message to raise if the record is found.

        Raises:
            CustomException: If the record is found in the database.

        Returns:
            dict: The result of the query.
        """
        get_data = {
            'model': model,
            'request': request
        }

        response = self.process_sql.get_data(
            **get_data
        )

        message = message if message else VALUE_NOT_EXISTS.format(get_primary_key(model))

        if not response:
            raise CustomException(message)
        
        return response

