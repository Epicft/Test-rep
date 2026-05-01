from typing import Optional
import aiosqlite
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db",
    echo=True
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class TaskOrm(Model):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(default=None)
    is_completed: Mapped[bool] = mapped_column(default=False)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_completed": self.is_completed
        }
    
    
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
            logger.info("Таблица создана или существует")
    except Exception as e:
        logger.error(f"Ошибка создания таблиц: {e}")
        raise
        

async def delete_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
            logger.info("Таблицы удалены")
    except Exception as e:
        logger.error(f"Ошибка удаления таблиц: {e}")
        raise