from Classes.Authentication import Authentication
from Utils.Authorizer import response_format

@response_format
def get_token(event, context):
    class_ = Authentication()
    methods = {
        "POST": class_.login,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
