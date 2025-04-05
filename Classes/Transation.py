from Utils.Response import ApiResponse
from http import HTTPStatus
from Utils.Tools.TypingTools import EventType
from Helpers.GeneralTools import get_input_data
from Helpers.BasicHelper import BasicHelper
from Helpers.ProcessSql import ProcessSql
from typing import List
from datetime import datetime

ACTIVE = 1

class Transaction:
    
    def __init__(self):
        self.process_sql = ProcessSql()
        self.bh = BasicHelper()

    def transation(self, event: EventType) -> ApiResponse:
        
        request = get_input_data(event)

        return ApiResponse(
            status_code=HTTPStatus.OK,
            data=request
        )
    