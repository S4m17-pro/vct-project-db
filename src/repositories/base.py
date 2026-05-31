import psycopg2.extras
from sqlalchemy import Engine


class BaseRepository:
    def __init__(self, engine: Engine):
        self._engine = engine

    def _call_proc(self, name: str, **kwargs):
        conn = self._engine.raw_connection()
        try:
            with conn.cursor() as cursor:
                ph = ", ".join("%s" for _ in range(len(kwargs)))
                cursor.execute(f"CALL {name}({ph})", list(kwargs.values()))
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _call_func(self, name: str, **kwargs):
        conn = self._engine.raw_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                ph = ", ".join("%s" for _ in range(len(kwargs)))
                cursor.execute(f"SELECT * FROM {name}({ph})", list(kwargs.values()))
                conn.commit()
                return [dict(r) for r in cursor.fetchall()]
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _call_func_one(self, name: str, **kwargs):
        rows = self._call_func(name, **kwargs)
        return rows[0] if rows else None
