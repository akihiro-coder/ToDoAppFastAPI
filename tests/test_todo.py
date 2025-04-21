import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

pytestmark = pytest.mark.asyncio


async def test_create_todo_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. ユーザーを登録
        await ac.post("/users/signup", json={
            "email": "test@example.com",
            "password": "test123"
        })

        # 2. ログインしてトークン取得
        login_res = await ac.post("/users/login", data={
            "username": "test@example.com",
            "password": "test123"
        })
        token = login_res.json()["access_token"]

        # 3. ヘッダーにトークンをセットしてToDo作成
        headers = {"Authorization": f"Bearer {token}"}
        todo_res = await ac.post("/todos/todos", json={
            "title": "Test Task",
            "description": "This is a test task.",
            "completed": False
        }, headers=headers)

        assert todo_res.status_code == 201
        assert todo_res.json()["title"] == "Test Task"


async def test_read_todo_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. ユーザー登録 & ログイン
        await ac.post("/users/signup", json={
            "email": "reader@example.com",
            "password": "test123"
        })
        login_res = await ac.post("/users/login", data={
            "username": "reader@example.com",
            "password": "test123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. ToDo作成（1件登録しておく）
        await ac.post("/todos/todos", json={
            "title": "Read Task",
            "description": "This is a task for read test.",
            "completed": False
        }, headers=headers)

        # 3. ToDo取得（一覧）
        res = await ac.get("/todos/todos", headers=headers)
        assert res.status_code == 200
        todos = res.json()
        assert isinstance(todos, list)
        assert any(todo["title"] == "Read Task" for todo in todos)


async def test_update_todo_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. ユーザー登録 & ログイン
        await ac.post("/users/signup", json={
            "email": "updater@example.com",
            "password": "test123"
        })
        login_res = await ac.post("/users/login", data={
            "username": "updater@example.com",
            "password": "test123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. ToDo作成
        create_res = await ac.post("/todos/todos", json={
            "title": "Old Title",
            "description": "Old Description",
            "completed": False
        }, headers=headers)
        todo_id = create_res.json()["id"]

        # 3. ToDo更新
        update_res = await ac.put(f"/todos/todos/{todo_id}", json={
            "title": "New Title",
            "description": "New Description",
            "completed": True
        }, headers=headers)

        assert update_res.status_code == 200
        updated = update_res.json()
        assert updated["title"] == "New Title"
        assert updated["description"] == "New Description"
        assert updated["completed"] is True


async def test_delete_todo_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. ユーザー登録 & ログイン
        await ac.post("/users/signup", json={
            "email": "deleter@example.com",
            "password": "test123"
        })
        login_res = await ac.post("/users/login", data={
            "username": "deleter@example.com",
            "password": "test123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. ToDo作成
        create_res = await ac.post("/todos/todos", json={
            "title": "To be deleted",
            "description": "This todo will be deleted",
            "completed": False
        }, headers=headers)
        todo_id = create_res.json()["id"]

        # 3. ToDo削除
        delete_res = await ac.delete(f"/todos/todos/{todo_id}", headers=headers)
        assert delete_res.status_code == 204  # ← No Content（削除成功）

        # 4. 再度取得 → 404を期待
        get_res = await ac.get(f"/todos/todos/{todo_id}", headers=headers)
        assert get_res.status_code == 404
