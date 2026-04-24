from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from database import TaskOrm, new_session
from models import STask, STaskAdd
from sqlalchemy import select


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
    ) -> list[STask]:
        try:
            async with new_session() as session:
                query = select(TaskOrm)
                if status:
                    query = query.where(TaskOrm.status == status)
                query = query.offset(skip).limit(limit)
                result = await session.execute(query)
                task_models = result.scalars().all()
                task_schemas = [STask.model_validate(task_model) for task_model in task_models]
                return task_schemas
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database query error:{str(e)}"
            )
            
    @classmethod
    async def mark_is_complete(
        cls,
        task_id: int
    ) -> bool:
        try:
            async with new_session() as session:
                result = await session.execute(
                    select(TaskOrm).where(TaskOrm.id == task_id)
                )
                task = result.scalars().one_or_none()
                if not task:
                    return False
                task.is_completed = True
                await session.commit()
                return True
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
                return STask.model_validate(task)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error when finding task: {str(e)}"
            )

    # @classmethod
    # async def delattr():
        # pass