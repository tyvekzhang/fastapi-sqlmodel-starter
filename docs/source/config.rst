Config
============

Project Info
---------

.. code-block:: none

    APP_NAME=Fss                    # The name of the application
    APP_DESC="Fss aims to be one... # A short description of the application
    MODE=dev                        # Deployment mode (e.g., dev, test, prod)
    PORT=9010                       # Port the application listens on
    WORKERS=1                       # The number of server workers
    API_VERSION=/api/v1             # The versioning prefix for the application's API endpoints

Time Zone
---------

.. code-block:: none

    WIN_TZ="China Standard Time"    # The time zone setting for Windows
    LINUX_TZ=Asia/Shanghai          # The time zone setting for Linux

Database
--------

.. code-block:: none

    # Uncomment the appropriate line for the desired database
    # SQLALCHEMY_DATABASE_URL=driver://user:pass@localhost:port/dbname
    SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:///./fss.db  # SQLite database using aiosqlite for asynchronous support
    # SQLALCHEMY_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:port/dbname
    # SQLALCHEMY_DATABASE_URL=mysql+aiomysql://user:pass@localhost:port/dbname

Cache
-----

.. code-block:: none

    ENABLE_REDIS=False              # Whether to use Redis for caching; if false, pagecache is used
    CACHE_HOST=127.0.0.1            # Host address for the cache server
    CACHE_PORT=6379                 # Port for the cache server
    CACHE_PASS=                     # Password for the cache server, if required

Extended Configuration
----------------------

.. code-block:: none

    ALGORITHM="HS256"               # The algorithm used to sign the JWT tokens
    SECRET_KEY=JtEaGi0RBPQ3ob-y4... # The secret key used for encoding JWT tokens
    ENABLE_SWAGGER=True             # Flag to enable or disable Swagger documentation
    LOG_FILE=/var/log/fss/log.txt   # Location of the log file
    BACKEND_CORS_ORIGINS="http://... # CORS origins setting, specifying which domains can make cross-origin requests
    WHITE_LIST_ROUTES="/api/v1/p... # List of API routes that do not require authorization