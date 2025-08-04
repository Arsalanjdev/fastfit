import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
SessionLocal = None


def init_db():
    global engine, SessionLocal
    if engine is not None:
        return

    ENV = os.getenv("ENV", "dev")

    # Only load .env file in non-test environments
    if ENV != "test":
        from pathlib import Path

        from dotenv import load_dotenv

        dotenv_path = Path(__file__).resolve().parent / ".env"
        if dotenv_path.exists():
            load_dotenv()

    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        # Only use individual variables in non-test environments
        if ENV != "test":
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_host = os.getenv("DB_HOST")
            db_name = os.getenv("DB_NAME")
            db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"
        else:
            raise RuntimeError("DATABASE_URL must be set in test environment")

    engine = create_engine(db_url, future=True, echo=(ENV == "dev"))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    if SessionLocal is None:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_engine():
    if engine is None:
        init_db()
    return engine
