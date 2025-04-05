import json
import datetime

DEFAULT_400_MESSAGE = "Missing or invalid parameters."

class ApiResponse():

    def __init__(self, 
                 status_code: int = 200, 
                 data: dict = [],
                 message: str = "",
                 excep=None):

        self.status_code = status_code
        self.excep = excep
        self.__prepare_body(message, data)

    # Build a internal format response
    def __prepare_body(self, message, data):

        match self.status_code:
            case 200:
                self.message = message if message else "The request was successfull."
                self.data = data
            case 201:
                self.message = message if message else "Resource created successfully."
                self.data = data
            case 204:
                self.message = message if message else "Resource updated successfully."
                self.data = data
            case 400:
                self.message = message if message else "A validation error ocurred."
                self.data = data if data else DEFAULT_400_MESSAGE
            case 401:
                self.message = message if message else "User not authenticated."
                self.data = data
            case 403:
                self.message = message if message else "User not authorized."
                self.data = data
            case 404:
                self.message = message if message else "Resource not found."
                self.data = data
            case 500:
                self.message = message if message else "Internal Server Error."
                self.data = data


    # Return a format lambda response
    def to_lambda_response(self):

        internal_reponse = {
            "status": self.status_code,
            "description": self.message,
            "data": self.data if self.data else []
        }

        api_response = {
            "statusCode": self.status_code,
            "headers": {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,'
                + 'UPDATE,DELETE',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With,'
                + ' Content-Type, Accept'
            },
            "body": json.dumps(internal_reponse, default=myconverter)
        }
        # Muestre de error por consola
        if self.status_code not in [200, 201]:
            if self.excep:
                print("¡Error! ", str(self.excep))
            else:
                print("¡Error Controlado! ", self.message)

        return api_response


def myconverter(o):

    if isinstance(o, datetime.date):
        return o._str_()