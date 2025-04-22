"""Customer exceptions"""

import http


class ServiceException(Exception):
    """
    Base service exception for handling service-related errors.

    Args:
        code: An integer representing the error code.
        msg: A string containing the error message.
        status_code: An optional integer representing the HTTP status code (default is 200 OK).
    """

    def __init__(self, code: int, msg: str, status_code: int = http.HTTPStatus.OK):
        """
        Initializes the ServiceException with the given parameters.

        Args:
            code: Error code indicating the model of error.
            msg: Error message providing details about the error.
            status_code: HTTP status code corresponding to the error (default is 200 OK).
        """
        self.code = code
        self.msg = msg
        self.status_code = status_code

    def __repr__(self) -> str:
        """
        Returns a string representation of the main configuration.

        Returns:
            str: A string representation of the instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class SystemException(ServiceException):
    """
    System module exception
    """

    def __init__(self, code: int, msg: str, status_code: int = http.HTTPStatus.OK):
        super(SystemException, self).__init__(code=code, msg=msg, status_code=status_code)


class SessionNotInitialisedException(Exception):
    """
    Exception raised when the user creates a new DB session without first initialising it.
    """

    def __init__(self):
        detail = """
        Session not initialised! Ensure that DBSessionMiddleware has been initialised before
        attempting database access.
        """

        super().__init__(detail)


class MissingSessionException(Exception):
    """
    Exception raised for when the user tries to access a database session before it is created.
    """

    def __init__(self):
        detail = """
        No session found! Either you are not currently in a request context,
        or you need to manually create a session context by using a `db` instance as
        a context manager e.g.:

        async with db():
            await db.session.execute(foo.select()).fetchall()
        """

        super().__init__(detail)


class ConfigNotInitialisedException(Exception):
    """
    Exception raised when the config not load correctly.
    """

    def __init__(self):
        detail = """
        Config not initialised! Ensure that config has been loaded before attempting.
        """

        super().__init__(detail)


class ParameterException(Exception):
    """
    Exception raised when parameter is error.
    """

    def __init__(self):
        detail = """
        Parameter error, please try again later.
        """

        super().__init__(detail)
