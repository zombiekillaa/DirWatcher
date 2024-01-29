from pydantic import BaseModel

from DirWatcher.settings import settings


class Config(BaseModel):
    directory: str
    interval: int  # Interval in seconds
    magic_string: str
    task_running: bool


config = Config(
    directory=settings.directory, interval=settings.interval,
    magic_string=settings.magic_string, task_running=settings.task_running
)
