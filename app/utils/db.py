from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from contextlib import contextmanager

engine = create_engine(
    settings.PG_CONN_STR,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    connect_args={"keepalives": 1, "keepalives_idle": 30}  # TCP keepalive settings
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        raise
    finally:
        db.close()