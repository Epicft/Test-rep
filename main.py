from contextlib import asynccontextmanager
from datetime import datetime
from aiosqlite import context
from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import select
from database import create_tables, delete_tables, TaskOrm, new_session
from repository import TaskRepository
from routers import tasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import traceback


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.middleware("http")
async def catch_all_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except TypeError as e:
        if "unhashable type" in str(e):
            print("Глобальная ошибка: попытка хешировать словарь")
            print("Трассировка:", traceback.format_exc())
            return HTMLResponse(
                "<h1>Ошибка рендеринга шаблона</h1><p>Проверьте данные и логику шаблона</p>",
                status_code=500
            )
        else:
            raise



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(tasks.router)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    try:
        tasks = await TaskRepository.find_all()
        context = {
            "request": request,  # ← это экземпляр запроса
            "tasks": tasks,
            "page_title": "Task Manager"
        }
            
        
        return templates.TemplateResponse(request=Request, name="index.html", context=context)
    except Exception as e:
        print(f"Ошибка в обработчике home_page: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки главной страницы: {e}")