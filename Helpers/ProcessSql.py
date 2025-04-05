from Utils.Database import Database
from Utils.Tools.QueryTools import get_columns, get_primary_key
from typing import List, Union, Dict
from Utils.Constants.ErrorMessages import (
    VALUE_NOT_EXISTS
)


class ProcessSql:
    def __init__(self):
        self.db = Database().session

    def insert(self, model: object)->int:
        """
        Inserts a new record into the database and returns the primary key of the new record.

        Args:
            model (object): The model to insert a new record into.

        Returns:
            int: The primary key of the new record.
        """
        self.db.add(model)
        self.db.commit()
        id_ = getattr(model, get_primary_key(model))

        # Close the database session
        self.db.close()

        return id_
    
    def update(self, 
            model: object, 
            conditions: dict, 
            values: dict
        )->int:
        """
        Updates records in the model based on the given conditions and values.

        Args:
            model (object): The model to update records from.
            conditions (dict): The conditions to filter the records to update.
            values (dict): The values to update the records with.

        Returns:
            int: The number of records updated.
        """

        res = self.db.query(model).filter_by(**conditions).update(values)
        self.db.commit()
        self.db.close()

        return res

    def get_data(self, 
                 model: object, 
                 request: dict = {},
                 like_filter: List[str] = [],
                 unequal_filter: List[str] = [],
                 columns: Union[List[str], None] = [],
                 all_columns_except: Union[List[str], None] = []
                 )->dict:
        """
        Retrieves records from the model based on the given conditions and
        filters the columns to return.

        Args:
            model (object): The model to retrieve records from.
            request (dict): The conditions to filter the records to retrieve.
            columns (List[str]): The columns to include in the result.

        Returns:
            dict: The result of the query, where the keys are the column names
                and the values are the values of the columns.
        """
        conditions = [
            getattr(model, 'active') == True
        ]

        limit = request.pop('limit', None)
        offset = request.pop('offset', None)

        for key, value in request.items():
            if key not in get_columns(model):
                raise KeyError('Invalid column: ' + key)
        
            if key in unequal_filter:
                conditions.append(getattr(model, key) != value)
            elif key in like_filter:
                conditions.append(getattr(model, key).like('%' + value + '%'))
            else:
                conditions.append(getattr(model, key) == value)


        if columns:
            columns = [getattr(model, column) for column in columns] if columns else [model]
        elif all_columns_except:
            columns = [getattr(model, column) for column in get_columns(model) if column not in all_columns_except]
        else:
            columns = [getattr(model, column) for column in get_columns(model)]

        # Create the query
        response = self.db.query(
            *columns
        ).filter(*conditions)

        # Set the limit and offset for the query
        if limit:
            response = response.limit(limit)
        if offset:    
            response = response.offset(offset)
        
        # Get the result of the query as a dictionary
        response = response.as_dict()
        print("response", response)

        # Close the database session
        self.db.close()

        return response
    
    def delete(self, model: object, conditions: dict)->int:
        """
        Deletes records from the model based on the given conditions.

        Args:
            model (object): The model to delete records from.
            conditions (dict): The conditions to filter the records to delete.

        Returns:
            int: The number of records deleted.
        """
        res = self.db.query(model).filter_by(**conditions).update({'active': False})
        self.db.commit()
        self.db.close()

        return res
    
    def validate_id(self, data:List[Dict[str, Union[object, int]]])->bool:
        """
        Validates the IDs in data list.

        Args:
            data (List[Dict[str, Union[object, int]]]): 
                A list of dictionaries. Each dictionary must have the following:
                - model (object): The model to validate the ID.
                - id (int): The ID to validate.
                - name (str): The name of the ID, used in error messages.

        Returns:
            bool: True if all IDs are valid, False otherwise.

        Raises:
            ValueError: If any ID is not valid.
        """
        for item in data:
            required = item.get('required', True)
            if required==False and not item['id']:
                continue
            model = item['model']
            id_ = item['id']
            name = item['name']
            pk = get_primary_key(model)
            # Check if the ID exists in the model
            response = self.db.query(model).filter(
                    getattr(model, pk)==id_
                ).first()
            self.db.close()

            if not response:
                # If the ID doesn't exist, raise an error
                raise ValueError(VALUE_NOT_EXISTS.format(name))
    
    


    
    