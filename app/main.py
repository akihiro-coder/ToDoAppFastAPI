import os
from dotenv import load_dotenv

# .envファイルの読み込み(load env file from the same directory as this file)
load_dotenv()


from app import models
from app.database import engine

# DBのテーブルを作成
models.Base.metadata.create_all(bind=engine)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Todo API",
    description="A simple Todo API using FastAPI and SQLite",
    version="1.0.0",
)

from app.routers import todos, users
# ルーターの登録
app.include_router(todos.router)
app.include_router(users.router)


# 静的ファイルの登録
app.mount("/static", StaticFiles(directory="app/static"), name="static")