import os
from functools import lru_cache

from src.main.app.common.config.config import (
    Config,
)
from src.main.app.common.config.config_loader import ConfigLoader
from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import (
    SystemException,
)
from src.main.app.common.util.work_path_util import resource_dir

config: Config


@lru_cache
def load_config() -> Config:
    """
    Loads the configuration based on the provided command-line arguments.

    Args:
        args (Namespace): Command-line arguments containing 'env' for the environment
                          and 'config_file' for the configuration file path.

    Returns:
        Config: A configuration object populated with the loaded settings.
    """
    global config
    env = os.getenv("ENV", "dev")

    config_file = os.getenv("CONFIG_FILE", None)
    config_loader = ConfigLoader(env, config_file)
    config_dict = config_loader.load_config()
    config = Config(config_dict)
    return config


def get_database_url(*, env: str = "dev"):
    assert env in ("dev", "prod", "local")
    config_path = os.path.join(resource_dir, f"config-{env}.yml")
    config_dict = ConfigLoader.load_yaml_file(config_path)
    if "database" not in config_dict:
        raise SystemException(
            ResponseCode.PARAMETER_ERROR.code,
            f"{ResponseCode.PARAMETER_ERROR.msg}: {env}",
        )
    return config_dict["database"]["url"]
