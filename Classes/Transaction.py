from Utils.Response import ApiResponse
from http import HTTPStatus
from Utils.Tools.TypingTools import EventType
from Utils.Constants.Constant import RETIRO, DEPOSITO
from Helpers.GeneralTools import get_input_data
from Utils.Tools.ValidationTools import validate_field
from Helpers.BasicHelper import BasicHelper
from Helpers.ProcessSql import ProcessSql
from Models.TransactionTypeModel import TransactionTypeModel
from Models.CorrespondentModel import CorrespondentModel
from Models.TransactionModel import TransactionModel
from Utils.CustomException import CustomException
import Schemas.TransactionSchemas as CreateTransactionSchema
from typing import TypedDict


class RequestTransaction(TypedDict):
    transaction_type_id: int
    correspondent_id: int
    amount: float

class Transaction:
    
    def __init__(self):
        self.process_sql = ProcessSql()
        self.basic_helper = BasicHelper()
        self.schemas = CreateTransactionSchema

    def transaction(self, event: EventType) -> ApiResponse:
        """
        Performs a financial transaction (deposit or withdrawal) for a correspondent.

        This method processes a transaction request by validating the existence of the
        transaction type and correspondent, updates the correspondent's available space
        based on the transaction type (deposit or withdrawal), and logs the transaction.

        Args:
            event (EventType): The input event containing transaction data. Must include:
                - transaction_type_id (int): ID of the transaction type (e.g., deposit or withdrawal).
                - correspondent_id (int): ID of the correspondent.
                - amount (float): Amount to be deposited or withdrawn.

        Returns:
            ApiResponse: A response object indicating the success of the operation,
            with updated available space and transaction details.

        Raises:
            CustomException: If the correspondent does not have enough available space
            for a withdrawal transaction.
        """

        request : RequestTransaction = get_input_data(event)
        validate_field(self.schemas.CreateTransactionSchema(), request)

        transaction_type_id = int(request['transaction_type_id'])
        correspondent_id = int(request['correspondent_id'])
        amount = float(request['amount'])

        self.basic_helper.validate_if_does_not_exist(TransactionTypeModel, {'transaction_type_id': transaction_type_id})
        self.basic_helper.validate_if_does_not_exist(CorrespondentModel, {'correspondent_id': correspondent_id})

        correspondent_data = self.process_sql.get_data(
            model=CorrespondentModel,
            request={'correspondent_id': correspondent_id},
            all_columns_except=['active', 'created_at', 'updated_at']
        )[0]

        transaction_type_data = self.process_sql.get_data(
            model=TransactionTypeModel,
            request={'transaction_type_id': transaction_type_id},
            all_columns_except=['created_at', 'updated_at', 'active']
        )[0]

        # Logic the operation type
        if transaction_type_data['transaction_type_id'] == RETIRO:
            if amount > correspondent_data['available_space']:
                raise CustomException("Cupo insuficiente para realizar el retiro")
            correspondent_data['available_space'] -= amount

        if transaction_type_data['transaction_type_id'] == DEPOSITO:
            correspondent_data['available_space'] += amount
 
        # Update Data Correspondent
        self.process_sql.update(
            model=CorrespondentModel,
            values={
                'available_space': correspondent_data['available_space']
            },
            conditions={'correspondent_id': correspondent_id}
        )

        # Registrar operación
        self.process_sql.insert(
            model=TransactionModel(**{
                'correspondent_id': correspondent_id,
                'transaction_type_id': transaction_type_id,
                'amount_to_withdraw': amount
            }),
        )

        return ApiResponse(
            status_code=HTTPStatus.OK,
            message="Operación realizada correctamente",
            data={
                "available_space": correspondent_data['available_space'],
                "operation_name": transaction_type_data['name'],
                "ammount": amount
            }
        )
    
