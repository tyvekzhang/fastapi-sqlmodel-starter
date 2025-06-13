Default Config
===============

Project Info
--------------

.. code-block:: none

    APP_NAME=Fast web
    APP_DESC="Fast web aims to one of the best scaffolding in the PyWeb field."
    VERSION=1.1.1
    MODE=prod
    HOST=0.0.0.0
    PORT=9010
    WORKERS=1
    API_VERSION=/api/v1
    ECHO_SQL=True
    ENABLE_SWAGGER=True
    LOG_FILE=../log/fast_web/log.txt

Time Zone
---------

.. code-block:: none

    WIN_TZ="China Standard Time"
    LINUX_TZ=Asia/Shanghai

Database
--------

.. code-block:: none

    #SQLALCHEMY_DATABASE_URL=driver://user:pass@localhost:port/dbname
    SQLALCHEMY_DATABASE_URL=sqlite+aiosqlite:///migrations/db/fast_web.db
    #SQLALCHEMY_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:port/dbname
    #SQLALCHEMY_DATABASE_URL=mysql+aiomysql://user:pass@localhost:port/dbname

Cache
-----

.. code-block:: none

    ENABLE_REDIS=False
    CACHE_HOST=127.0.0.1
    CACHE_PORT=6379
    CACHE_PASS=
    DB_NUM=0

Security
----------------------

.. code-block:: none

    ALGORITHM="HS256"
    SECRET_KEY=JtEaGi0RBPQ3ob-y4ZHzCwX8JLe_aPiWiQTUYGu58k4
    ACCESS_TOKEN_EXPIRE_MINUTES=1440
    REFRESH_TOKEN_EXPIRE_MINUTES=43200
    WHITE_LIST_ROUTES="/api/v1/probe/liveness, /api/v1/probe/readiness, /api/v1/user/login, /api/v1/user/register"

Middleware
----------------------

.. code-block:: none

    BACKEND_CORS_ORIGINS="http://127.0.0.1, http://localhost:3000, http://localhost"
    BLACK_IP_LIST=""
    ENABLE_RATE_LIMIT=True
    GLOBAL_DEFAULT_LIMITS="10/second"
