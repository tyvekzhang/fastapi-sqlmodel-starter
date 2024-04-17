from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    expired_at: int
    refresh_token: str
    re_expired_at: int


class CurrentUser(BaseModel):
    user_id: int
    roles: set = Field(default_factory=set)
    authorities: set = Field(default_factory=set)
