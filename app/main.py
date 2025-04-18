from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import todos, users


# DBのテーブルを作成
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Todo API",
    description="A simple Todo API using FastAPI and SQLite",
    version="1.0.0",
)


# ルーターの登録
app.include_router(todos.router)
app.include_router(users.router)