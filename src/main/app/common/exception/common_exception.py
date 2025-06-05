"""Common module exception"""

from fastapi import FastAPI

from src.main.app.common.exception import exception_handler


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers to the FastAPI application"""

    # Register handlers using add_exception_handler method
    app.add_exception_handler(Exception, exception_handler.global_exception_handler)


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
