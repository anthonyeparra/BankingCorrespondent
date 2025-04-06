from Helpers.ProcessSql import ProcessSql
from Utils.Tools.TypingTools import EventType
from Utils.Response import ApiResponse
from Helpers.GeneralTools import get_input_data
from Models.TransactionTypeModel import TransactionTypeModel
from Models.CorrespondentModel import CorrespondentModel
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
    
    def get_transation_type(self, event: EventType) -> ApiResponse:
        """
        Retrieves transaction type data based on the input event.

        This method extracts filter conditions from the input event and calls `get_resources`
        with the TransactionTypeModel to return the matching transaction type data.

        Args:
            event (EventType): The event object containing request data (filter conditions).

        Returns:
            ApiResponse: An ApiResponse object containing the transaction type data and an HTTP status code of OK.
        """
        request = get_input_data(event)
        return self.get_resources(model=TransactionTypeModel, request=request)
    
    def get_correspondent(self, event:EventType) -> ApiResponse:
        """
        Retrieves correspondent data based on the input event.

        This method extracts filter conditions from the input event and calls `get_resources`
        with the CorrespondentModel to return the matching correspondent data.

        Args:
            event (EventType): The event object containing request data (filter conditions).

        Returns:
            ApiResponse: An ApiResponse object containing the correspondent data and an HTTP status code of OK.
        """
        request = get_input_data(event)
        return self.get_resources(model=CorrespondentModel, request=request)
    
