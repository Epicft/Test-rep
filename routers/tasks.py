from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from models import STaskAdd, STask, STaskId
from repository import TaskRepository


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks

@router.post("")
async def create_task(task: STaskAdd
) -> STaskId:
    print(f"{task} --- это таска")
    task_id = await TaskRepository.add_one(task)
    print(f"{task} --- это таска")
    return {"ok": True, "task_id": task_id}

@router.put("/{task_id}/complete")
async def complete_task(task_id: int) -> STask:
    updated_task = await TaskRepository.mark_is_complete(task_id)
    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return updated_task    
    
    
@router.delete("/{task_id}")
async def del_task(task_id: int):
    try:
        repo = TaskRepository()
        deleted_task = await repo.delete_task(task_id)
        if deleted_task:
            return {"ok": True, "message": "Task deleted"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}") 