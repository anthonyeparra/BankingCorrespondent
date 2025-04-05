from marshmallow import ValidationError
from Utils.CustomException import CustomException

def validate_field(schema, data:dict):
    try:
        schema.load(data)
    except ValidationError as err:
        raise CustomException(
            list(err.messages.values())[0][0],
        )