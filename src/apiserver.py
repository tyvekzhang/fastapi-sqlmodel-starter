"""Main entrance of the project"""

import argparse
import os
import sys
import uvicorn

# Add the project path to the system path for module imports
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, os.pardir, os.pardir)
project_path = os.path.abspath(project_dir)
sys.path.insert(0, project_path)

parser = argparse.ArgumentParser(description="Custom arguments for the server")
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
