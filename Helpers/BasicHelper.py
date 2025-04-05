from Utils.CustomException import CustomException
from Helpers.ProcessSql import ProcessSql
from Utils.Constants.ErrorMessages import (
    VALUE_ALREADY_EXISTS,
    RELATIONSHIP_NOT_EXISTS,
    VALUE_NOT_EXISTS
)
from typing import Union
from Utils.Tools.QueryTools import get_primary_key
import requests
import deepl
import os

class BasicHelper:
    def __init__(self):
        self.process_sql = ProcessSql()

    def validate_city_state(
            self, 
            models: list, 
            city_id: int, 
            state_id: int,
            country_id: int,
            )->None:
        """
        Validate the existence of a city-state-country relationship in the database.

        Args:
            models (list): List containing city and state models.
            city_id (int): The ID of the city to validate.
            state_id (int): The ID of the state to validate.
            country_id (int): The ID of the country to validate.

        Raises:
            CustomException: If the city-state or state-country relationship does not exist.
        """
        
        city_model = models[0]
        state_model = models[1]
        
        # Validate the state exists within the specified country
        state_validation = self.process_sql.get_data(
            model=state_model,
            request={
                'state_id': state_id,
                'country_id': country_id
            },
            columns=['state_id']
        )

        # Validate the city exists within the specified state
        city_validation = self.process_sql.get_data(
            model=city_model,
            request={
                'city_id': city_id,
                'state_id': state_id
            },
            columns=['city_id']
        )

        if not city_validation:
            raise CustomException(
                RELATIONSHIP_NOT_EXISTS.format('city_id', 'state_id')
            )

        if not state_validation:
            raise CustomException(
                RELATIONSHIP_NOT_EXISTS.format('state_id', 'country_id')
            )

    def validate_functions(
            self,
             model, 
             request: dict,
             type_: str = 'create',
             function_id: Union[int, None] = None
             )->None:
        """
        Validate the existence of a function in the database.

        Args:
            model (object): The model to validate the function in.
            data (dict): The data to validate. It should contain the keys 'path' and 'method'.
            type_ (str): The type of validation. It can be 'create' or 'update'.
            function_id (int): The ID of the function to update. It is only used when type_ is 'update'.

        Raises:
            CustomException: If the function already exists in the database.
        """
        
        path = request.get('path')
        method = request.get('method')

        like_filters = []
        if path:
            like_filters.append('path')
        if method:
            like_filters.append('method')

        get_data = {
            'model': model,
            'request': request,
            'like_filter': like_filters,
            'columns': ['function_id']
        }

        if type_ == 'update':
            request['function_id'] = function_id
            get_data['unequal_filter'] = ['function_id']

        response =self.process_sql.get_data(
            **get_data
        )

        if response:
            raise CustomException(
                VALUE_ALREADY_EXISTS.format('function')
            )
        
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
        
    def open_weather_api(self, lat, lon):
        """
        Get the current weather from the Open Weather API.

        Given the latitude and longitude, it will return the current weather
        for that location.

        Parameters
        ----------
        lat : float
            The latitude of the location.
        lon : float
            The longitude of the location.

        Returns
        -------
        response : requests.Response
            The response from the Open Weather API.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "lang": "es",
            "appid": os.getenv('OPEN_WEATHER_API_KEY'),
            "units": "metric",
        }

        response = requests.get(os.getenv('OPEN_WEATHER_API_URL'), params=params)

        return response.json()
    
    def translate_service(self, text, target):
        """
        Translates the given text to the specified target language using the DeepL service.

        Parameters
        ----------
        text : str
            The text to be translated.
        target : str
            The target language code (e.g., 'EN' for English, 'DE' for German).

        Returns
        -------
        str
            The translated text.
        """

        auth_key = os.getenv('DEEPL_API_KEY')
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target)

        return result.text
