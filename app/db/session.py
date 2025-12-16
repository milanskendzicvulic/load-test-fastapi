from typing import Any, Generator
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from sqlalchemy.orm.session import Session

from app.config.settings import settings

engine: Engine = create_engine(
    url=settings.POSTGRES_DSN,
    pool_pre_ping=True,
    echo=False, 
    pool_size=10,  
    max_overflow=12,
)

SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, autoflush=False)


def get_session() -> Generator[Session, Any, None]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


session_context = contextmanager(func=get_session)
