from .base import BaseRepository


class AuthRepository(BaseRepository):
    def autenticar(self, username: str, password: str):
        return self._call_func_one("sp_autenticar_usuario", p_username=username, p_password=password)

    def registrar(self, username: str, password: str, rol: str = "Auditor"):
        self._call_proc("sp_registrar_usuario", p_username=username, p_password=password, p_rol=rol)
