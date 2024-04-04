from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer",
    expired_at: int
    refresh_token: str
    re_expired_at: int
