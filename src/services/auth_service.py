from datetime import datetime, timedelta, timezone
import jwt

from ..config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
from ..repositories.auth_repo import AuthRepository


class AuthService:
    def __init__(self, repo: AuthRepository):
        self._repo = repo

    def login(self, username: str, password: str):
        user = self._repo.autenticar(username, password)
        if not user:
            return None
        token = self._generar_token(user["username"], user["rol_usuario"])
        return {
            "username": user["username"],
            "privilegios": user["rol_usuario"],
            "token": token,
        }

    def register(self, username: str, password: str, rol: str = "Auditor"):
        self._repo.registrar(username, password, rol)

    def _generar_token(self, username: str, role: str) -> str:
        payload = {
            "sub": username,
            "role": role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
