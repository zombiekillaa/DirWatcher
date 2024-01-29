from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from DirWatcher.db.dependencies import get_db
from DirWatcher.db.models.task_run import TaskRunModel
from DirWatcher.db.session import SessionLocal


class TaskRunDAO:
    """Class for accessing TaskRun table."""

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_task_run_model(
        self, start_time: datetime, end_time: datetime,
        total_runtime: int, files_added: List[str], files_deleted: List[str],
        magic_string_count: int, directory: str, magic_string: str, status: str
    ) -> None:
        """
        Add single TaskRun to session.
        """
        self.session.add(
            TaskRunModel(
                start_time=start_time, end_time=end_time, total_runtime=total_runtime,
                files_added=files_added, files_deleted=files_deleted,
                magic_string_count=magic_string_count, directory=directory,
                magic_string=magic_string, status=status
            )
        )

    def get_all_task_runs(self, limit: int, offset: int) -> List[TaskRunModel]:
        """
        Get all TaskRun models with limit/offset pagination.

        :param limit: limit of task_runs.
        :param offset: offset of task_runs.
        :return: stream of task_runs.
        """
        raw_task_runs = self.session.execute(
            select(TaskRunModel).limit(limit).offset(offset),
        )

        return list(raw_task_runs.scalars().fetchall())

    def filter(
        self,
        limit: int, offset: int,
        directory: Optional[str] = None,
        magic_string: Optional[str] = None,

    ) -> List[TaskRunModel]:
        """
        Get specific TaskRun model.

        :param limit: limit of task_runs.
        :param offset: offset of task_runs.
        :param directory: directory of TaskRun instance.
        :param magic_string: magic_string of TaskRun instance.
        :return: TaskRun models.
        """
        query = select(TaskRunModel)
        if magic_string:
            query = query.where(TaskRunModel.magic_string == magic_string)
        if directory:
            query = query.where(TaskRunModel.directory == directory)

        rows = self.session.execute(query.limit(limit).offset(offset))
        return list(rows.scalars().fetchall())

    # Database CRUD operations
    def create_task_run(self, task_run: TaskRunModel):
        self.session.add(task_run)
        self.session.commit()
        self.session.refresh(task_run)

    def get_latest_task_run(self, directory: Optional[str] = None) -> TaskRunModel:
        query = self.session.query(TaskRunModel)
        if directory:
            query = query.filter(TaskRunModel.directory == directory)
        return query.order_by(
            TaskRunModel.start_time.desc()).first()


task_run_dao = TaskRunDAO(SessionLocal())
