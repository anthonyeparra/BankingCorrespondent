from Classes.Transaction import Transaction
from Utils.Authorizer import authorizer

@authorizer 
def test(event, context):
    class_ = Transaction()
    methods = {
        "POST": class_.transation,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
