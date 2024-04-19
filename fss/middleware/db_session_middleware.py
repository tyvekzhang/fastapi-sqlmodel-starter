"""Session proxy used in the project"""

from contextvars import ContextVar
from typing import Dict, Optional, Union

from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from fss.common.config import configs
from fss.starter.server import app

try:
    from sqlalchemy.ext.asyncio import async_sessionmaker
except ImportError:
    from sqlalchemy.orm import sessionmaker as async_sessionmaker


def create_middleware_and_session_proxy():
    _Session: Optional[async_sessionmaker] = None
    # Usage of context vars inside closures is not recommended, since they are not properly
    # garbage collected, but in our use case context var is created on program startup and
    # is used throughout the whole its lifecycle.
    _session: ContextVar[Optional[AsyncSession]] = ContextVar("_session", default=None)

    class SQLAlchemyMiddleware(BaseHTTPMiddleware):
        def __init__(
            self,
            app: ASGIApp,
            db_url: Optional[Union[str, URL]] = None,
            custom_engine: Optional[Engine] = None,
            engine_args: Dict = None,
            session_args: Dict = None,
            commit_on_exit: bool = True,
        ):
            super().__init__(app)
            self.commit_on_exit = commit_on_exit
            engine_args = engine_args or {}
            session_args = session_args or {}

            if not custom_engine and not db_url:
                raise ValueError(
                    "You need to pass a db_url or a custom_engine parameter."
                )
            if not custom_engine:
                engine = create_async_engine(db_url, **engine_args)
            else:
                engine = custom_engine

            nonlocal _Session
            _Session = async_sessionmaker(
                engine, class_=AsyncSession, expire_on_commit=False, **session_args
            )

        async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
            async with DBSession(commit_on_exit=self.commit_on_exit):
                return await call_next(request)

    class DBSessionMeta(type):
        @property
        def session(self) -> AsyncSession:
            """Return an instance of Session local to the current async context."""
            if _Session is None:
                raise SessionNotInitialisedException

            session = _session.get()
            if session is None:
                raise MissingSessionException

            return session

    class DBSession(metaclass=DBSessionMeta):
        def __init__(self, session_args: Dict = None, commit_on_exit: bool = False):
            self.token = None
            self.session_args = session_args or {}
            self.commit_on_exit = commit_on_exit

        async def __aenter__(self):
            if not isinstance(_Session, async_sessionmaker):
                raise SessionNotInitialisedException

            self.token = _session.set(_Session(**self.session_args))  # type: ignore
            return type(self)

        async def __aexit__(self, exc_type, exc_value, traceback):
            session = _session.get()

            try:
                if exc_type is not None:
                    await session.rollback()
                elif (
                    self.commit_on_exit
                ):  # Note: Changed this to elif to avoid commit after rollback
                    await session.commit()
            finally:
                await session.close()
                _session.reset(self.token)

    return SQLAlchemyMiddleware, DBSession


SQLAlchemyMiddleware, db = create_middleware_and_session_proxy()


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


# Add SQLAlchemyMiddleware
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(configs.sqlalchemy_database_url),
    engine_args={
        "echo": configs.echo_sql,
    },
)
