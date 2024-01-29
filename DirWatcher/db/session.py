from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from DirWatcher.settings import settings

engine = create_engine(
    settings.db_url_sync.__str__(), pool_pre_ping=True, poolclass=NullPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
