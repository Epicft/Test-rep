from fastapi import FastAPI
from routers import tasks

app = FastAPI(
    title='Мой первый api проект',
    description='API с хабра',
    version='1.0.0'
)


app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать! /docs для документации"}
