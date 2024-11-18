"""The main entrance of the program"""

import argparse
import os

from main.server import run

parser = argparse.ArgumentParser(description="Custom arguments for the server")
parser.add_argument(
    "-e",
    "--env",
    type=str,
    default="dev",
    help="Specify the environment for the project",
)
args = parser.parse_args()
os.environ["ENV"] = args.env

if __name__ == "__main__":
    run()
