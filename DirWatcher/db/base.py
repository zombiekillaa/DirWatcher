from sqlalchemy.orm import DeclarativeBase

from DirWatcher.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
