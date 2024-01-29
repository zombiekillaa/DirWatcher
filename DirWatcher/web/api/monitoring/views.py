from fastapi import APIRouter

from DirWatcher.config import config

router = APIRouter()


@router.get("/health")
def health_check() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
    return {"message": "UP", "status": 200, "dir_watcher_running": config.task_running}
