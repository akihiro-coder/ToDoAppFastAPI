from pydantic import BaseModel
from typing import Optional


# Base: リクエスト用(POST, PUTなど)
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


# 作成用（クライアントから受け取るデータ）
class TodoCreate(TodoBase):
    pass


# レスポンス用（DBのIDを含む）
class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True # ORMのデータからPydanticモデルへ変換可能に
