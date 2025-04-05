import json
from Utils.Response import ApiResponse
from Utils.CustomException import CustomException
from sqlalchemy.exc import SQLAlchemyError
from Helpers.GeneralTools import verify_token
import traceback


def response_format(function_to_run):

    def wrapper(*args, **kwargs):

        try:
            response = function_to_run(*args, **kwargs)

        except KeyError as ke:
            get_traceback_info(ke)
            response = ApiResponse(400, str(ke))
        except Warning as wa:
            get_traceback_info(wa)
            response = ApiResponse(400, str(wa))
        except ValueError as ve:
            get_traceback_info(ve)
            response = ApiResponse(400, str(ve))
        except TypeError as te:
            get_traceback_info(te)
            response = ApiResponse(400, excep=te)
        except CustomException as ce:
            get_traceback_info(ce)
            data = ce.message
            response = ApiResponse(400, data, excep=ce)
        except SQLAlchemyError as sql_excep:
            get_traceback_info(sql_excep)
            response = ApiResponse(400, str(sql_excep.orig))
        except Exception as e:
            get_traceback_info(e)
            response = ApiResponse(500, str(e), excep=e)
        try:
            return response.to_lambda_response()
            
        except Exception as e:
            get_traceback_info(e)
            response = ApiResponse(500, excep=e)
            lambda_response = response.to_lambda_response()

        return lambda_response

    return wrapper

def authorizer(function_to_run):

    def wrapper(*args, **kwargs):

        try:
            # event: dict = args[0]
            # token: str = event['headers'].get('Authorization')
            # if token:
            #     user_data = verify_token(token.split(' ')[1])
            #     event['user_id'] = user_data['user_id']
            # else:
            #     raise CustomException("No token provided", 401)
            
            response = function_to_run(*args, **kwargs)

        except KeyError as ke:
            get_traceback_info(ke)
            response = ApiResponse(400, str(ke))
        except Warning as wa:
            get_traceback_info(wa)
            response = ApiResponse(400, str(wa))
        except ValueError as ve:
            get_traceback_info(ve)
            response = ApiResponse(400, str(ve))
        except TypeError as te:
            get_traceback_info(te)
            response = ApiResponse(400, excep=te)
        except CustomException as ce:
            get_traceback_info(ce)
            data = ce.message
            response = ApiResponse(ce.code, data, excep=ce)
        except SQLAlchemyError as sql_excep:
            get_traceback_info(sql_excep)
            response = ApiResponse(400, str(sql_excep.orig))
        except Exception as e:
            get_traceback_info(e)
            response = ApiResponse(500, str(e), excep=e)
        try:
            return response.to_lambda_response()
            
        except Exception as e:
            get_traceback_info(e)
            response = ApiResponse(500, excep=e)
            lambda_response = response.to_lambda_response()

        return lambda_response

    return wrapper

def get_traceback_info(exc) -> None:
    trace = traceback.extract_tb(exc.__traceback__)
    error_lines = []
    exc_type = type(exc).__name__
    exc_message = str(exc)
    for row in trace:
        error_lines.append({
            "filename": row.filename,
            "method": row.name,
            "lineno": row.lineno,
            "code": row.line.strip() if row.line else ""
        })
    
    error_info = {
        "exception": {
            "trace": [
                {
                    "type": exc_type,
                    "message": exc_message,
                    "lines": error_lines
                }
            ]
        }
    }

    print(json.dumps(error_info, indent=4))
