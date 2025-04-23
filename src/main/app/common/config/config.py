import os.path
from os import makedirs


class ServerConfig:
    def __init__(
        self,
        host: str = "127.0.0.1",
        name: str = "Server",
        port: int = 18000,
        version: str = "0.1.0",
        app_desc: str = "Server",
        api_version: str = "/v1",
        workers: int = 1,
        log_file_path: str = "../log/fss/log.txt",
        win_tz: str = "China Standard Time",
        linux_tz: str = "Asia/Shanghai",
        enable_rate_limit: bool = False,
        global_default_limits: str = "10/second",
    ) -> None:
        """
        Initializes server configuration with default host and port.

        Args:
            host (str): The server host address. Default is '127.0.0.1'.
            name (str): The server name. Default is 'Server'.
            port (int): The server port number. Default is 18000.
            version (str): The server version. Default is '0.1.0'.
            app_desc (str): The server app_desc. Default is 'server'.
            api_version (str): The server api_version. Default is 'v1'.
            workers (int): The server worker numbers. Default is 1.
            log_file_path (str): Path to the log file. Default is '../log/fss/log.txt'.
            win_tz (str): Windows timezone setting. Default is 'China Standard Time'.
            linux_tz (str): Linux timezone setting. Default is 'Asia/Shanghai'.
            enable_rate_limit (bool): Whether to enable rate limiting. Default is False.
            global_default_limits (str): Global rate limit setting. Default is '10/second'.
        """
        self.host = host
        self.name = name
        self.port = port
        self.version = version
        self.app_desc = app_desc
        self.api_version = api_version
        self.workers = workers
        self.log_file_path = log_file_path
        self.win_tz = win_tz
        self.linux_tz = linux_tz
        self.enable_rate_limit = enable_rate_limit
        self.global_default_limits = global_default_limits

    def __repr__(self) -> str:
        """
        Returns a string representation of the server configuration.

        Returns:
            str: A string representation of the ServerConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class DatabaseConfig:
    def __init__(
        self,
        dialect: str = "sqlite",
        db_name="fss.db",
        url: str = "",
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 1800,
        echo_sql: bool = True,
        pool_pre_ping: bool = True,
        enable_redis: bool = False,
        cache_host: str = "127.0.0.1",
        cache_port: int = 6379,
        cache_pass: str = "",
        db_num: int = 0,
    ) -> None:
        """
        Initializes database configuration with a default database entity.

        Args:
            dialect (str): The entity of database. Default is 'sqlite'.
            db_name (str): The name of sqlite database. Default is 'server.db'.
            url (str): The url of database. Default is 'src/main/resource/alembic/db/server.db'.
            pool_size (int): The pool size of database. Default is 10.
            max_overflow (int): The max overflow of database. Default is 20.
            pool_recycle (int): The pool recycle of database. Default is 1800 sec.
            echo_sql (bool): Whether to echo sql statements. Default is True.
            pool_pre_ping (bool): Whether to pre ping. Default is True.
            enable_redis (bool): Whether to enable Redis cache. Default is False.
            cache_host (str): Redis host address. Default is '127.0.0.1'.
            cache_port (int): Redis port number. Default is 6379.
            cache_pass (str): Redis password. Default is empty.
            db_num (int): Redis database number. Default is 0.
        """
        self.dialect = dialect
        self.db_name = db_name
        if dialect == "sqlite" and url == "":
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_dir = os.path.join(base_dir, os.pardir, os.pardir, os.pardir, "resource", "alembic", "db")
            db_dir = os.path.abspath(db_dir)
            if not os.path.exists(db_dir):
                os, makedirs(db_dir)
            bd_path = os.path.join(db_dir, self.db_name)
            url = "sqlite+aiosqlite:///" + str(bd_path)
        self.url = url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.echo_sql = echo_sql
        self.pool_pre_ping = pool_pre_ping
        self.enable_redis = enable_redis
        self.cache_host = cache_host
        self.cache_port = cache_port
        self.cache_pass = cache_pass
        self.db_num = db_num

    def __repr__(self) -> str:
        """
        Returns a string representation of the database configuration.

        Returns:
            str: A string representation of the DatabaseConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class SecurityConfig:
    def __init__(
        self,
        enable: bool = True,
        enable_swagger: bool = False,
        algorithm: str = "HS256",
        secret_key: str = "43365f0e3e88863ff5080ac382d7717634a8ef72d8f2b52d436fc9847dbecc64",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_minutes: int = 43200,
        white_list_routes: str = "/v1/probe/liveness, /v1/probe/readiness, /v1/user/login, /v1/user/add, /v1/user/refreshTokens, /v1/user/export",
        backend_cors_origins: str = "http://127.0.0.1:8200, http://localhost:8200, http://localhost",
        black_ip_list: str = "",
    ) -> None:
        """
        Initializes security configuration with default values for algorithm,
        secret key, and token expiration durations.

        Args:
            enable (bool): Whether to enable security. Default is True.
            enable_swagger (bool): Whether to enable swagger ui. Default is False.
            algorithm (str): The encryption algorithm used for token generation.
                             Default is 'HS256'.
            secret_key (str): The secret key used for signing the tokens.
                              Default is a predefined key.
            access_token_expire_minutes (int): The number of minutes until the access
                                              token expires. Default is 30 minutes.
            refresh_token_expire_minutes (int): The number of minutes until the refresh
                                           token expires. Default is 43200 minutes.
            white_list_routes (str): Comma-separated list of routes which can be accessed
                                    without authentication. Default includes common probe and user routes.
            backend_cors_origins (str): Comma-separated list of allowed CORS origins.
                                       Default includes common local development URLs.
            black_ip_list (str): Comma-separated list of blocked IP addresses. Default is empty.
        """
        self.enable = enable
        self.enable_swagger = enable_swagger
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        self.white_list_routes = white_list_routes
        self.backend_cors_origins = backend_cors_origins
        self.black_ip_list = black_ip_list

    def __repr__(self) -> str:
        """
        Returns a string representation of the security configuration.

        Returns:
            str: A string representation of the SecurityConfig instance,
                 showing all configuration attributes and their current values.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class Config:
    def __init__(self, config_dict=None):
        if "server" in config_dict:
            self.server = ServerConfig(**config_dict["server"])
        else:
            self.server = ServerConfig()
        if "database" in config_dict:
            self.database = DatabaseConfig(**config_dict["database"])
        else:
            self.database = DatabaseConfig()
        if "security" in config_dict:
            self.security = SecurityConfig(**config_dict["security"])
        else:
            self.security = SecurityConfig()

    def __repr__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            str: A string representation of the config instance,
                 showing all configuration attributes and their current values.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
