# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Use when performing database migration"""

import importlib
from pathlib import Path
from typing import Dict, Type, Any, List, Optional

# List of directories to scan for model files
MODEL_PACKAGES = [
    "src/main/app/models",
]


def import_sql_models(packages: Optional[List[str]] = None) -> Dict[str, Type[Any]]:
    """Dynamically import all model classes from specified packages.

    Scans for Python files matching '*_model.py' pattern in each package directory.
    Model classes are identified by names ending with 'Model'.

    Args:
        packages: List of package paths to search. If None, uses default MODEL_PACKAGES.

    Returns:
        Dictionary mapping class names to class objects for all imported models.
    """
    packages_to_scan = packages or MODEL_PACKAGES
    imported_models = {}

    for package_path in packages_to_scan:
        package_dir = Path(package_path)

        if not package_dir.exists():
            print(f"Warning: Package directory not found: {package_dir}")
            continue

        for model_file in package_dir.glob("*_model.py"):
            try:
                # Convert path to module import format (e.g., "src/main/app/models/file_model")
                module_path = str(model_file.with_suffix('')).replace('/', '.')
                module = importlib.import_module(module_path)

                for name in dir(module):
                    if name.endswith("Model"):
                        model_class = getattr(module, name)
                        imported_models[name] = model_class

            except ImportError as e:
                print(f"Failed to import module {module_path}: {e}")
            except Exception as e:
                print(f"Unexpected error processing {module_path}: {e}")

    return imported_models


# Import models from default packages
imported_models = import_sql_models()

# Alternatively, import from specific packages:
# imported_models = import_models(["custom/package/models", "another/package/models"])

# For Alembic startup
ALEMBIC_START_SIGNAL = "Welcome! autogenerate is processing!"
