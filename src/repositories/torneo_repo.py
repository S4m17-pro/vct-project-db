from .base import BaseRepository


class TorneoRepository(BaseRepository):
    def obtener_todos(self):
        return self._call_func("sp_obtener_torneos")
