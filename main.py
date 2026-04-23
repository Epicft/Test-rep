from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables
from routers import tasks



@asynccontextmanager
async def lifespan(app:FastAPI):
    await delete_tables()
    print("Очистка базы")
    await create_tables()
    print("База готова")
    yield
    print('выключение')

app = FastAPI(lifespan=lifespan,
              title = "Задачник",
              description = "Простой задачник",
              version="1.1.0"              
              
              )


app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать, это просто Таски. /docs для документации"}
