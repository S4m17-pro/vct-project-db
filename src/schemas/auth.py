from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password_hash: str


class LoginResponse(BaseModel):
    username: str
    privilegios: str
    token: str
    status: Optional[str] = None


class RegisterRequest(BaseModel):
    username: str
    password_hash: str
    rol_usuario: str = "Auditor"
