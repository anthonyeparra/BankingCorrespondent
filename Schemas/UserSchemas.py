from marshmallow import Schema, fields

class CreateUserSchema(Schema):
    first_name = fields.String(
        required=True,
        error_messages={
            'required': 'First name is required.'
        }
    )
    last_name = fields.String(
        required=True,
        error_messages={
            'required': 'Last name is required.'
        }
    )
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
    active = fields.Integer(required=False)

