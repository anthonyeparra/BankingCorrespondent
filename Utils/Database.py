from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.pool import QueuePool
from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List
import os


class CustomQuery(Query):
    def as_dict(self) -> List[Dict[str, Any]]:
        """
        Devuelve los resultados de una consulta como una lista de diccionarios.
        Maneja tanto filas completas de modelos como resultados con columnas específicas.
        """
        results = []
        for row in self:
            # Si es una instancia de un modelo, utiliza `__table__.columns`
            if hasattr(row, '__table__'):
                result = {
                    column.name: (
                        getattr(row, column.name).isoformat()
                        if column.type.python_type in (datetime, date) and getattr(row, column.name) is not None
                        else getattr(row, column.name)
                    )
                    for column in row.__table__.columns
                }
            else:
                # Si no es una instancia de un modelo, es un objeto Row
                result = {
                    key: value.isoformat() if isinstance(value, (datetime, date))
                    else float(value) if isinstance(value, Decimal)
                    else value
                    for key, value in row._mapping.items()
                }
            results.append(result)
        return results

class Database:
    base_class = declarative_base()

    def __init__(self):
        connection_string = self.__get_connection_strings()
        self.__engine = create_engine(connection_string, poolclass=QueuePool)
        self.__session_maker = sessionmaker(bind=self.__engine, query_cls=CustomQuery)
        self.session = self.__session_maker()

    def __get_connection_strings(self):

        string = "mysql+pymysql://{}:{}@{}/{}".format(
            os.getenv('DB_USER'),
            os.getenv('DB_PASSWORD'),
            os.getenv('DB_HOST'),
            os.getenv('DB_NAME'))
        
        return string
    