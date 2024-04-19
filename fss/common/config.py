"""Configuration in the project"""

import multiprocessing
import os
import subprocess
import time
from typing import Union
from loguru import logger
from pathlib import Path as path

from pydantic.v1 import BaseSettings

current_file_path = os.path.abspath(__file__)
env_directory = path(current_file_path).parent.parent

ENV_FILE = os.path.join(env_directory, ".env")
if not os.path.exists(ENV_FILE):
    ENV_FILE = os.path.join(env_directory, ".env.example")


class Configs(BaseSettings):
    app_name: str
    app_desc: str
    mode: str
    version: str
    host: str
    port: int
    access_token_expire_minutes: int = 60 * 24
    refresh_token_expire_minutes: int = 60 * 24 * 30
    win_tz: str
    linux_tz: str
    workers: Union[str, int]
    backend_cors_origins: str
    white_list_routes: str
    algorithm: str
    secret_key: str
    log_file: str
    api_version: str
    sqlalchemy_database_url: str
    enable_redis: bool
    cache_pass: str
    cache_host: str
    cache_port: str
    db_num: int
    enable_swagger: bool
    echo_sql: bool

    class Config:
        env_file = ENV_FILE


configs = Configs()


def init_log():
    logger.add(configs.log_file)


# Set timezone
if os.name == "nt":
    try:
        subprocess.run(["tzutil", "/s", configs.win_tz], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting timezone: {e}")
else:
    try:
        os.environ["TZ"] = configs.linux_tz
        time.tzset()
    except Exception as e:
        logger.error(f"Error setting timezone: {e}")


def server_startup_config() -> tuple[str, int, int]:
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
