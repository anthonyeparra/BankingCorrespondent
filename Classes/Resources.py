from Helpers.ProcessSql import ProcessSql
from Utils.Tools.TypingTools import EventType
from Utils.Response import ApiResponse
from Helpers.GeneralTools import get_input_data
from Models.TransationTypeModel import TransationType
from Models.CorrespondentModel import Correspondent
from http import HTTPStatus

class Resources:
    def __init__(self):
        self.process_sql = ProcessSql()

    def get_resources(self, model, request:dict) -> ApiResponse:

        """
        Retrieves data from a given model based on the given request.

        Args:
            model (object): The model to retrieve data from.
            request (dict): The conditions to filter the data to retrieve.

        Returns:
            ApiResponse: The response object containing the status code and data.
        """
        data = self.process_sql.get_data(
            model=model,
            request=request,
            all_columns_except=['active', 'created_at', 'updated_at']
        )

        return ApiResponse(
            data=data,
            status_code=HTTPStatus.OK
        )
    
    def get_transation_type(self, event:EventType)->ApiResponse:
        request = get_input_data(event)
        return self.get_resources(model=TransationType, request=request)
    
    def get_correspondent(self, event:EventType)->ApiResponse:
        request = get_input_data(event)
        return self.get_resources(model=Correspondent, request=request)
    
