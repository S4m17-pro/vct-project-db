from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import Engine

from ..database import get_session
from ..dependencies import get_db
from ..schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from ..models.schema import Usuario
from ..services.auth_service import AuthService
from ..repositories.auth_repo import AuthRepository

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse)
def login(request_data: LoginRequest, engine: Engine = Depends(get_db)):
    service = AuthService(AuthRepository(engine))
    result = service.login(request_data.username, request_data.password_hash)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    result["status"] = "Login exitoso"
    return result


@router.post("/register")
def register(request_data: RegisterRequest, engine: Engine = Depends(get_db),
             session: Session = Depends(get_session)):
    existing = session.exec(select(Usuario).where(Usuario.username == request_data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    service = AuthService(AuthRepository(engine))
    service.register(request_data.username, request_data.password_hash, request_data.rol_usuario)
    return {"message": "Usuario creado con éxito", "usuario": request_data.username}
