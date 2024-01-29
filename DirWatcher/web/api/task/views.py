import asyncio
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, Query
from loguru import logger

from DirWatcher.config import config
from DirWatcher.db.dao.task_run_dao import TaskRunDAO
from DirWatcher.tasks.background_task import background_task
from DirWatcher.web.api.task.schema import ConfigDTO, TaskRunOutputDTO

router = APIRouter()


@router.put("/config")
async def update_config(input_config: ConfigDTO):
    logger.debug(f"Exising Configuration: {config}")
    config.directory = input_config.directory
    config.magic_string = input_config.magic_string
    config.interval = input_config.interval
    logger.info(f"Final Configuration: {config}")
    return {"message": "Configuration updated successfully"}


@router.get("/run")
async def get_all_task_run(
    task_run_dao: TaskRunDAO = Depends(),
    offset: int = Query(0, description="Skip the number of tasks"),
    limit: int = Query(
        100, description="Limit the number of tasks which needs to be brought"),
    directory: Optional[str] = Query(
        None, description="Fetch the latest task run for given directory"),
    magic_string: Optional[str] = Query(
        None, description="Fetch the latest task run for given directory"),
) -> List[TaskRunOutputDTO]:
    # Fetch latest task run details from the database
    task_runs = task_run_dao.filter(limit, offset, directory, magic_string)
    return [TaskRunOutputDTO(**task.__dict__) for task in task_runs]


@router.get("/latest_run")
async def get_latest_task_run(
    task_run_dao: TaskRunDAO = Depends(),
    directory: Optional[str] = Query(
        None, description="Fetch the latest task run for given directory"),
    ignore_directory: bool = Query(False, description="To skip search via directory")
) -> TaskRunOutputDTO:
    # Fetch latest task run details from the database
    if ignore_directory:
        # Ignore the directory and fetch the latest run
        task_run = task_run_dao.get_latest_task_run()
        return TaskRunOutputDTO(**task_run.__dict__)
    if not directory:
        # Default to the current directory on which DirWatcher is working
        directory = config.directory
    task_run = task_run_dao.get_latest_task_run(directory)
    return TaskRunOutputDTO(**task_run.__dict__)


@router.post("/start")
async def start_task():
    if config.task_running:
        raise HTTPException(status_code=400, detail="Task is already running")
    else:
        config.task_running = True
    asyncio.create_task(background_task())
    return {"message": "Task started successfully"}


@router.delete("/stop")
async def stop_task():
    if not config.task_running:
        raise HTTPException(status_code=400, detail="Task is not running")

    config.task_running = False
    return {"message": "Task stopped successfully"}
