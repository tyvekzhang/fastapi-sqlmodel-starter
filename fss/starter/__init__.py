"""Add project to python path"""

import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = str(Path(current_dir).parent.parent)
sys.path.insert(0, project_dir)
