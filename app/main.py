import os
from dotenv import load_dotenv

# .envファイルの読み込み(load env file from the same directory as this file)
load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env"))


from app import models
from app.database import engine

# DBのテーブルを作成
models.Base.metadata.create_all(bind=engine)


from fastapi import FastAPI

app = FastAPI(
    title="Todo API",
    description="A simple Todo API using FastAPI and SQLite",
    version="1.0.0",
)

from app.routers import todos, users
# ルーターの登録
app.include_router(todos.router)
app.include_router(users.router)