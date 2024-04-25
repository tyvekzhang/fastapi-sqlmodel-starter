"""Configuration in the project"""

import multiprocessing
import os
import subprocess
import time
from loguru import logger
from pathlib import Path as path

from pydantic.v1 import BaseSettings
from typing import Tuple

current_file_path = os.path.abspath(__file__)
env_directory = path(current_file_path).parent.parent

ENV_FILE = os.path.join(env_directory, ".env")
if not os.path.exists(ENV_FILE):
    ENV_FILE = os.path.join(env_directory, ".env.example")


class Configs(BaseSettings):
    app_name: str
    app_desc: str
    version: str
    mode: str
    host: str
    port: int
    workers: int
    api_version: str
    echo_sql: bool
    log_file: str
    enable_swagger: bool
    win_tz: str
    linux_tz: str
    sqlalchemy_database_url: str
    enable_redis: bool
    cache_host: str
    cache_port: int
    cache_pass: str
    db_num: int
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    white_list_routes: str
    backend_cors_origins: str
    black_ip_list: str
    enable_rate_limit: bool
    global_default_limits: str

    class Config:
        env_file = ENV_FILE


configs = Configs()


def init_log():
    logger.add(configs.log_file)


# Set timezone
if os.name == "nt":
    subprocess.run(["tzutil", "/s", configs.win_tz], check=True)

else:
    os.environ["TZ"] = configs.linux_tz
    time.tzset()


def server_startup_config() -> Tuple[str, int, int]:
    """
    Server startup config
    """
    host = configs.host
    port = configs.port
    workers = configs.workers
    if not isinstance(workers, int):
        workers = (
            int(workers)
            if workers.isdigit()
            else max(multiprocessing.cpu_count() - 2, 1)
        )
    return host, port, workers
