"""Configuration in the project"""

import os
import subprocess
import time
from typing import Union, Tuple
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
    port: int
    pool_size: int
    win_tz: str
    linux_tz: str
    workers: Union[str, int]
    backend_cors_origins: str
    secret_key: str
    log_file: str
    api_version_v1: str
    sqlalchemy_database_url: str

    class Config:
        env_file = ENV_FILE


configs = Configs()


def init_log() -> None:
    logger.add(configs.log_file)


def init_tz() -> None:
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


def complete() -> Tuple[int, int]:
    port = configs.port
    workers = configs.workers

    if not isinstance(workers, int):
        try:
            workers = int(workers)
        except ValueError:
            import multiprocessing

            cpu_count = multiprocessing.cpu_count()
            workers = max(cpu_count - 2, 1)
    return port, workers
