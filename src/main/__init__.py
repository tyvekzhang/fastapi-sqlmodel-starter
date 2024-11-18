"""Add project to python path"""

import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = str(Path(current_dir).parent.parent)
sys.path.insert(0, project_dir)

from src.common.exception import exception_handler  # noqa
from src.middleware import db_session_middleware  # noqa
from src.middleware import ip_block_middleware  # noqa
from src.middleware import rate_limit_middleware  # noqa
from src.main.system.router import system  # noqa
