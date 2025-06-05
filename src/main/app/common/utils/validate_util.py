from typing import Optional
from pydantic import BaseModel, ValidationError


class ValidateService:
    @staticmethod
    def validate(obj: BaseModel) -> Optional[str]:
        try:
            # 调用 Pydantic 的验证逻辑（适用于 Pydantic v2.x）
            obj.model_validate()  # 对于 v2.x 的 Pydantic
            return None
        except ValidationError as e:
            # 拼接错误信息
            errors = ", ".join([f"{'->'.join(map(str, error['loc']))}: {error['msg']}" for error in e.errors()])
            return errors

    @staticmethod
    def get_validate_err_msg(e: ValidationError) -> Optional[str]:
        err_msg = []
        for error in e.errors():
            field = " -> ".join(map(str, error["loc"]))  # 字段路径
            message = error["msg"]  # 错误描述
            err_msg.append(f"Error in field '{field}': {message}")
        return ",".join(err_msg)
