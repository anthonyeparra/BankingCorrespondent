from marshmallow import Schema, fields

class GetAuth(Schema):
    password = fields.String(
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required.'
        }
    )

