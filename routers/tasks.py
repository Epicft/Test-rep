from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from models import STaskAdd, STask, STaskId
from repository import TaskRepository


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


local_database = []


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks

@router.post("")
async def create_task(task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}

@router.post("/{task_id}/complete")
async def complete_task(task_id: int) -> STask:
    success = await TaskRepository.mark_is_complete(task_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    completed_task = await TaskRepository.find_by_id(task_id)
    return completed_task    
    
    
# @router.delete('')
# async def delete_task(task_delete: Annotated[STaskId, Depends()]):
#     task_del = await TaskRepository.delattr(task_delete)
#     return {'ok': 'Задача удалена', "task_del": task_del}
           