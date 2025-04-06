from marshmallow import Schema, fields

class CreateTransactionSchema(Schema):
    transaction_type_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'Transaction type id is required.'
        }
    )
    correspondent_id = fields.Integer(
        required=True,
        error_messages={
            'required': 'Correspondent is required.'
        }
    )
    amount = fields.Float(
        required=True,
        error_messages={
            'required': 'amount is required.'
        }
    )
 

