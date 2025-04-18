from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLiteファイルに保存
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# connect_argsはSQLite固有の設定（マルチスレッド回避）
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラス（モデル定義のベースになる）
Base = declarative_base()

# 依存関数: リクエスト毎にDBセッションを提供
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
