from sqlmodel import SQLModel

from faslava.enums.enums import CRUDOperationEnum


def base_crud_service(model: SQLModel, operation: CRUDOperationEnum, ):
    pass
