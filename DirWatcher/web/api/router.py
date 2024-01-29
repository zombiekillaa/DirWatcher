from fastapi.routing import APIRouter

from DirWatcher.web.api import docs, monitoring, task

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(task.router, prefix="/task", tags=["task"])
