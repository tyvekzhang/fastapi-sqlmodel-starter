from enum import Enum


class ResponseCode(Enum):
    """
    Enum for system response codes.
    """

    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "Service internal error")

    PARAMETER_ERROR = (400, "Parameter error")
    NO_IMPORT_DATA_ERROR = (400, "No import data detected")
    DUPLICATE_USERNAME_ERROR = (400, "Duplicate username")
    PASSWORD_VALID_ERROR = (
        400,
        "Password must contain digit, letter and length more than 6",
    )
    DB_UNKNOWN_ERROR = (400, "Db unknown error")
    AUTH_FAILED = (403, "Username or password error")
    PARAMETER_CHECK_ERROR = (402, "Parameter error")
    DATABASE_ALREADY_EXIST = (409, "Database already exist")
    UNSUPPORTED_DIALECT_ERROR = (500, "Unsupported dialect error")
    TABLE_EXISTS_ERROR = (400, "Table already exist, please remove it firstly")
    TEMPLATE_NOT_FOUND_ERROR = (500, "Template not found")
    USER_NAME_EXISTS = (100, "Username already exists")
    ROLE_ALREADY_EXISTS = (101, "Assign role already exists")

    @property
    def code(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]


class ConstantCode:
    """
    Enum for system constant codes.
    """

    USER_KEY = "user:"
    AUTH_KEY = "Authorization"
    UTF_8 = "utf-8"


class FilterOperators:
    """
    过滤条件的操作符常量
    """

    EQ = "EQ"  # 等于
    NE = "NE"  # 不等于
    GT = "GT"  # 大于
    GE = "GE"  # 大于等于
    LT = "LT"  # 小于
    LE = "LE"  # 小于等于
    BETWEEN = "BETWEEN"  # 介于
    LIKE = "LIKE"  # 模糊匹配


class SortEnum(str, Enum):
    """
    Enum for specifying sorting order.
    """

    ascending = "asc"
    descending = "desc"


class TokenTypeEnum(str, Enum):
    """
    Enum for token entity.
    """

    access = "access"
    refresh = "refresh"
    bearer = "Bearer"


class DBTypeEnum(str, Enum):
    """
    Enum for database type.
    """

    PGSQL = "postgresql"
    MYSQl = "mysql"
    SQLITE = "sqlite"
