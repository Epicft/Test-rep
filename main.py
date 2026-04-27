from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from database import create_tables, delete_tables
from routers import tasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os



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

app.mount("/static", StaticFiles(directory="static"), name="static")
#templates = Jinja2Templates(directory="templates")
app.include_router(tasks.router)

@app.get("/", response_class=HTMLResponse)
async def home_page():
    template_path = os.path.join("templates", "index.html")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        print(f"Ошибка чтения шаблона: {e}")
        raise HTTPException(status_code=500, detail="Ошибка загрузки главной страницы")