from sqlalchemy import Column, func, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class UsersModel(Base):

    __tablename__ = 'users'

    user_id=Column(Integer, primary_key=True)
    first_name=Column(String(50), nullable=True)
    last_name=Column(String(50), nullable=True)
    email=Column(String(50), nullable=True)
    password=Column(String(250), nullable=True)
    active=Column(Integer, nullable=True, default=str(1))
    created_at=Column(DateTime, nullable=True, default=func.current_timestamp())
    updated_at=Column(DateTime, nullable=True, default=func.current_timestamp())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)