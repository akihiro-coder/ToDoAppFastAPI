from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Todoの一覧取得
@app.get("/todos", response_model=list[schemas.Todo])
def read_todos(skip: int = 0,  limit: int = 10, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos


# Todoの作成
@app.post("/todos", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.model_dump())
    try:
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'DB Error: {str(e)}')


# 詳細取得
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todoが見つかりませんでした。")
    return todo

# 更新
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, updated_todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todoが見つかりません。")

    # 値を上書き
    todo.title = updated_todo.title
    todo.description = updated_todo.description
    todo.completed = updated_todo.completed

    try:
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'DB Error: {str(e)}')


# 削除
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todoが見つかりません。")

    try:
        db.delete(todo)
        db.commit()
        return {"message": "削除しました。"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'DB Error: {str(e)}')