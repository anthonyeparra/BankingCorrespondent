from Classes.BankCorrespondent import BankCorrespondent
from Utils.Authorizer import authorizer

@authorizer 
def test(event, context):
    class_ = BankCorrespondent()
    methods = {
        "GET": class_.get,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
