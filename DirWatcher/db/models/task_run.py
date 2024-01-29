from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from DirWatcher.db.base import Base


class TaskRunModel(Base):
    __tablename__ = "task_runs"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column("start_time", TIMESTAMP(timezone=True), nullable=False)
    end_time = Column("end_time", TIMESTAMP(timezone=True), nullable=False)
    total_runtime = Column("total_runtime", Integer, nullable=True)
    files = Column("files", JSONB, nullable=True)
    files_added = Column("files_added", JSONB, nullable=True)
    files_deleted = Column("files_deleted", JSONB, nullable=True)
    magic_string_count = Column("magic_string_count", Integer, nullable=True)
    directory = Column("directory", String(64), nullable=True)
    magic_string = Column("magic_string", String(64), nullable=True)
    status = Column("status", String(64), nullable=True)
