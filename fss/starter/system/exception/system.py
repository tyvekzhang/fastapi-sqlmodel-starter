"""System exception"""

import http

from fss.common.exception.exception import ServiceException


class SystemException(ServiceException):
    """
    System module exception
    """

    def __init__(self, code: int, msg: str, status_code: int = http.HTTPStatus.OK):
        super(SystemException, self).__init__(
            code=code, msg=msg, status_code=status_code
        )
