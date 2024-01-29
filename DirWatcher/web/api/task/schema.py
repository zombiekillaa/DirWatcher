from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ConfigDTO(BaseModel):
    directory: Optional[str]
    interval: Optional[int]
    magic_string: Optional[str]


class ConfigOutputDTO(ConfigDTO):
    task_running: Optional[bool]


class TaskRunInputDTO(BaseModel):
    start_time: datetime
    end_time: datetime
    total_runtime: int
    files_added: List[str]
    files_deleted: List[str]
    magic_string_count: int
    status: str


class TaskRunOutputDTO(BaseModel):
    start_time: datetime
    end_time: datetime
    total_runtime: Optional[int]
    files: Optional[List[str]]
    files_added: Optional[List[str]]
    files_deleted: Optional[List[str]]
    directory: Optional[str]
    magic_string: Optional[str]
    magic_string_count: Optional[int]
    status: str
