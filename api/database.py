import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
#URL de conexão com o banco de dados baseado nas variáveis de ambiente
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.environ['DATABASE_USER']}:"
    f"{os.environ['DATABASE_PASSWORD']}@"
    f"{os.environ['DATABASE_HOST']}:"
    f"{os.environ['DATABASE_PORT']}/"
    f"{os.environ['DATABASE_NAME']}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()