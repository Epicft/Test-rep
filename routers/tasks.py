from fastapi import APIRouter, HTTPException, Depends
from models import Task


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


local_database = []

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
        return {"q": q, "skip": skip, "limit": limit}

@router.get("")
def get_tasks(pagination: dict = Depends(common_parameters)):
    skip = pagination["skip"]
    limit = pagination["limit"]
    return common_parameters[skip : skip + limit]

@router.post("")
def create_task(task: Task):
    new_task = task.model_dump()
    new_task["id"] = len(local_database) + 1
    local_database.append(new_task)
    
@router.delete('/{task_id}')
def delete_task(task_id: int):
    for idx, t in enumerate(local_database):
        if t['id'] == task_id:
            del local_database[idx]
            return {'message': 'Задача {idx} удалена'}
    raise HTTPException(status_code=404, detail="Задача не найдена")