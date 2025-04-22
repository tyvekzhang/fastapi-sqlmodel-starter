import os
import yaml

from typing import Dict


class ConfigLoader:
    def __init__(self, env: str, base_config_file: str = None) -> None:
        """
        Initializes a new instance of the ConfigLoader class

        Args:
            env (str): Store the environment (e.g., 'dev', 'prod')
            base_config_file (str): Store the base config file path
        """
        if base_config_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, os.pardir, os.pardir, os.pardir, "resource", "config.yml")
            base_config_file = os.path.abspath(config_path)
            self.default_flag = True
        self.base_config_file = base_config_file
        self.config = {}
        self.env = env

    @staticmethod
    def load_yaml_file(file_path) -> Dict:
        """
        Load a YAML file and return its contents as a dictionary.

        Args:
            file_path (str): The path to the YAML file to be loaded.

        Returns:
            Dict: The contents of the YAML file as a dictionary.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def merge_dicts(self, base_dict, override_dict) -> Dict:
        """
        Merge two dictionaries, with values from the override_dict taking precedence.

        Args:
            base_dict (Dict): The base dictionary to merge values into.
            override_dict (Dict): The dictionary containing values to override.

        Returns:
            Dict: The merged dictionary.
        """
        if override_dict is None:
            return base_dict
        for key, value in override_dict.items():
            if isinstance(value, dict) and key in base_dict:
                # If the value is a dictionary, recursively merge it
                base_dict[key] = self.merge_dicts(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    def load_config(self, environment: str = None) -> Dict:
        """
        Load the base configuration file and merge it with environment-specific settings if available.

        Args:
            environment (str, optional): The specific environment to load settings for.
                                          If None, defaults to the instance's environment.

        Returns:
            Dict: The final merged configuration.
        """
        self.config = self.load_yaml_file(self.base_config_file)
        if self.default_flag:
            if not environment:
                environment = self.env
            env_config_file = f"config-{environment}.yml"
            # Replace the base config file name with the environment-specific one
            env_config_path = self.base_config_file.replace("config.yml", env_config_file)
            if os.path.exists(env_config_path):
                env_config = self.load_yaml_file(env_config_path)
                self.config = self.merge_dicts(self.config, env_config)

        return self.config

    def get_config(self) -> Dict:
        """
        Return the loaded configuration.

        Returns:
            Dict: The configuration loaded and merged from the base and environment-specific files.
        """
        return self.config
