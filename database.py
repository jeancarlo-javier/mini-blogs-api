import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base, Session as _Session
from sqlalchemy.engine import Engine
from sqlite3 import Connection
from contextlib import contextmanager

ENV = os.getenv("ENV", "development")
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

db_url = ""
if ENV == "production":
    db_url = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
else:
    db_url = "sqlite:///./local_database.db"

engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=True)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def _enable_foreing_keys(dbapi_connection: Connection, connection_record: Connection):
    dbapi_connection.execute("PRAGMA foreign_keys=ON")

event.listen(engine, "connect", _enable_foreing_keys)

@contextmanager
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()