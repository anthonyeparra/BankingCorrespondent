from Classes.Transaction import Transaction
from Utils.Authorizer import authorizer

@authorizer 
def transaction(event, context):
    class_ = Transaction()
    methods = {
        "POST": class_.transaction,
        "GET": class_.get_transaction,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
