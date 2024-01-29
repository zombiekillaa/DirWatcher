import asyncio
import os
from datetime import datetime

from loguru import logger

from DirWatcher.config import config
from DirWatcher.db.dao.task_run_dao import task_run_dao
from DirWatcher.db.models.task_run import TaskRunModel


async def background_task():
    while config.task_running:
        directory = config.directory
        interval = config.interval
        magic_string = config.magic_string

        logger.debug(f"Background Task Started. Config: {config}")
        try:
            start_time = datetime.now()

            # Fetch the existing files from the database
            last_run = task_run_dao.get_latest_task_run(directory)
            existing_files = last_run.files if last_run else []

            files_in_directory = os.listdir(directory)
            files_added = [f for f in files_in_directory if f not in existing_files]
            files_deleted = [f for f in existing_files if f not in files_in_directory]

            magic_string_count = 0
            # Iterate over the files and search for the magic string
            for filename in files_in_directory:
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as file:
                        content = file.read()
                        magic_string_count += content.count(magic_string)

            end_time = datetime.now()
            total_runtime = (end_time - start_time).total_seconds()

            task_run = TaskRunModel(
                start_time=start_time,
                end_time=end_time,
                total_runtime=total_runtime,
                files=files_in_directory,
                files_added=files_added,
                files_deleted=files_deleted,
                directory=directory,
                magic_string=magic_string,
                magic_string_count=magic_string_count,
                status="Success"  # Update status accordingly
            )
            logger.debug(f"Background Task Completed Successfully. Config: {config}")
            logger.info(f"Result: {task_run.__str__()}")
            task_run_dao.create_task_run(task_run)
        except Exception as e:
            logger.error(f"{e}")
            logger.exception(e)
            end_time = datetime.now()
            total_runtime = (end_time - start_time).total_seconds()
            # Log error and update status as "Failed"
            task_run = TaskRunModel(
                start_time=start_time,
                end_time=end_time,
                total_runtime=total_runtime,
                files_added=None,
                files_deleted=None,
                directory=directory,
                magic_string=magic_string,
                magic_string_count=None,
                status="Failed"  # Update status accordingly
            )
            task_run_dao.create_task_run(task_run)

        # Sleep for configured interval before starting the next cycle
        await asyncio.sleep(interval)
