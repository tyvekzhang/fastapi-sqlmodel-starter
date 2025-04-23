"""Main entrance of the project"""

import argparse
import os
import sys

import uvicorn


def find_project_root(marker_file="pyproject.toml"):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir

        parent_dir = os.path.dirname(current_dir)

        if parent_dir == current_dir:
            raise FileNotFoundError(f"Could not find {marker_file} in any parent directory")

        current_dir = parent_dir


project_dir = find_project_root()
sys.path.insert(0, project_dir)

parser = argparse.ArgumentParser(description="Custom arguments for this server")
parser.add_argument(
    "-e",
    "--env",
    type=str,
    default="dev",
    help="Specify the environment for the project",
)
parser.add_argument(
    "-c",
    "--config_file",
    type=str,
    default=None,
    help="Path to a custom configuration file",
)
args = parser.parse_args()

os.environ["ENV"] = args.env
if args.config_file:
    os.environ["CONFIG_FILE"] = args.config_file


# Load the configuration and run the server
def main():
    from src.main.app.common.config.config_manager import load_config

    server_config = load_config().server
    app_name = "src.main.app.server:app"
    host = server_config.host
    port = server_config.port
    workers = server_config.workers
    uvicorn.run(app=app_name, host=host, port=port, workers=workers)


if __name__ == "__main__":
    main()
