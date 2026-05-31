from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import jwt

from .config import JWT_SECRET, JWT_ALGORITHM
from .database import get_session, engine
from .repositories.auth_repo import AuthRepository

security = HTTPBearer()

def get_db():
    return engine

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def require_role(role: str):
    async def checker(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return user
    return checker
