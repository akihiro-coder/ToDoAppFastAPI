from pydantic import BaseModel, EmailStr
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
class TodoOut(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True # ORMのデータからPydanticモデルへ変換可能に



# 登録リクエスト用
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# レスポンス用
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
