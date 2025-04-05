from Classes.Resources import Resources
from Utils.Authorizer import authorizer


@authorizer
def transation_type(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_transation_type
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)


@authorizer
def correspondent(event, context):
    class_ = Resources()
    methods = {
        "GET": class_.get_correspondent
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)



