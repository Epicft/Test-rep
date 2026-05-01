from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from database import TaskOrm, new_session
from models import STask, STaskAdd
from sqlalchemy import delete, select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        try:
            async with new_session() as session:
                task_dict = data.model_dump()

                task = TaskOrm(**task_dict)
                session.add(task)
                await session.flush()
                await session.commit()
                return task.id
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error:{str(e)}"
            )
    
    @classmethod
    async def find_all(
        cls,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None
    ) -> list[dict]:
        try:
            async with new_session() as session:
                print("Выполняем запрос к БД...")
                result = await session.execute(select(TaskOrm))
                tasks_orm = result.scalars().all()
                print(f"Получено задач из БД: {len(tasks_orm)}")

                # Проверяем преобразование каждой задачи
                taskslist = []
                for i, task in enumerate(tasks_orm):
                    try:
                        task_dict = task.to_dict()
                        print(f"Задача {i} успешно преобразована: {task_dict}")
                        taskslist.append(task_dict)
                    except Exception as e:
                        print(f"Ошибка преобразования задачи {i}: {e}")
                        raise

            print("Все задачи успешно преобразованы")
            return taskslist
        except Exception as e:
            print(f"Критическая ошибка в get_all_tasks: {e}")
            raise
            
    @classmethod
    async def mark_is_complete(
        cls,
        task_id: int
    ) -> STask | None:
        try:
            async with new_session() as session:
                result = await session.execute(
                    select(TaskOrm).where(TaskOrm.id == task_id)
                )
                task = result.scalars().one_or_none()
                if not task:
                    return None
                task.is_completed = True
                await session.commit()
                await session.refresh(task)
                return task.to_dict()
        except SQLAlchemyError as e:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
    
    
    @classmethod
    async def find_by_id(
        cls,
        task_id: int
    ) -> STask | None:
        try:
            async with new_session() as session:
                result = await session.execute(
                    select(TaskOrm).where(TaskOrm.id == task_id)
                )
                task = result.scalars().one_or_none()
                if not task:
                    return None
                return task.to_dict()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error when finding task: {str(e)}"
            )

    @staticmethod
    async def delete_task(task_id: int) -> bool:
        try:
            async with new_session() as session:
                result = await session.execute(
                    select(TaskOrm).where(TaskOrm.id == task_id)
                )
                task_delete = result.scalar_one_or_none()
                
                await session.delete(task_delete)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error when finding task: {str(e)}")