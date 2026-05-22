
from sqlmodel import create_engine, Session

# Credenciales reales de tu docker-compose
DB_USER = "admin"
DB_PASSWORD = "vctLS"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "vct_stats"

DATABASE_URL = f"postgresql://admin:vctLS@localhost:5432/vct_stats"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


