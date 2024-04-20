"""Add project to python path"""

import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = str(Path(current_dir).parent.parent)
sys.path.insert(0, project_dir)

from fss.common.exception import exception_handler  # noqa
from fss.middleware import db_session_middleware  # noqa
from fss.middleware import ip_block_middleware  # noqa
from fss.middleware import rate_limit_middleware  # noqa
from fss.starter.system.router import system  # noqa
