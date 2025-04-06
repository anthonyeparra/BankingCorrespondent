from Classes.Users import Users
from Utils.Authorizer import response_format

@response_format
def users(event, context):
    class_ = Users()
    methods = {
        "POST": class_.create_user
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)


