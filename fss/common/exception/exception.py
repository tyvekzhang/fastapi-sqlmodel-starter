"""The exceptions used in the project"""

import http
from typing import Any, Dict, Optional

from fastapi import HTTPException


class ClientBaseException(HTTPException):
    """
    An HTTP exception you can raise in your own code to show errors to the client.
    """

    def __init__(
        self,
        status_code: Optional[int] = http.HTTPStatus.BAD_REQUEST,
        detail: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthException(ClientBaseException):
    """
    Exception raised for when the user's username or password.
    """

    def __init__(self):
        detail = """
        Incorrect username or password
        """
        super().__init__(status_code=http.HTTPStatus.UNAUTHORIZED, detail=detail)


class LockException(ClientBaseException):
    """
    Exception raised for when the user's username or validation message incorrect.
    """

    def __init__(self):
        detail = """
        Your account is locked, Please contact the  administrator
        """
        super().__init__(status_code=http.HTTPStatus.UNAUTHORIZED, detail=detail)


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
