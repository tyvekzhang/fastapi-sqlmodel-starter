"""Customer exceptions"""

import http


class ServiceException(Exception):
    def __init__(self, code: int, msg: str, status_code: int = http.HTTPStatus.OK):
        """
        Base service exception
        :param code: error code
        :param msg: error message
        :param status_code: http status code
        """
        self.code = code
        self.msg = msg
        self.status_code = status_code
