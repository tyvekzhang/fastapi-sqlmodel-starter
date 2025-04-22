"""Use when performing database migration"""

import importlib
from pathlib import Path

# 定义模型所在的目录
MODELS_DIR = Path("src/main/app/model")


# 动态导入所有模型类
def import_models():
    for model_file in MODELS_DIR.glob("*_model.py"):
        module_name = f"src.main.app.model.{model_file.stem}"
        module = importlib.import_module(module_name)
        for name in dir(module):
            if name.endswith("DO"):  # 假设所有模型类以 DO 结尾
                globals()[name] = getattr(module, name)


# 执行动态导入
import_models()

# 用于 Alembic 的启动信号
start_signal = "Welcome! autogenerate is processing!"
