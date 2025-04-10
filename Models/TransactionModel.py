from sqlalchemy import Column, func, String, Integer, TIMESTAMP, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TransactionModel(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_type_id = Column(Integer, nullable=False)
    correspondent_id = Column(Integer, nullable=False)
    amount_to_withdraw = Column(DECIMAL(12,2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    active = Column(Integer, default=1)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)