from enum import Enum


class EnvEnum(str, Enum):
    DEV = "dev"
    QUAL = "qual"
    PRE_PROD = "pre-prod"
    PROD = "prod"


class CRUDOperationEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    FILTER = "filter"
    SELECT_ONE = "select_one"


class APIResponseStatusEnum(str, Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
