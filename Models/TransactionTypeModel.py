from sqlalchemy import Column, func, String, Integer, TIMESTAMP, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransactionType(Base):
    __tablename__ = 'transaction_type'

    transaction_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    active = Column(Integer, default=1)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)