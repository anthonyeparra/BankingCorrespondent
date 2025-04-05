from typing import List

def get_columns(model)-> List[str]:
    return model.__table__.columns.keys()

def get_primary_key(model)-> str:
    return model.__table__.primary_key.columns[0].name
