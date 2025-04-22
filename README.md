# 🚀 ToDo API – FastAPI Practice

[![CI](https://github.com/akihiro-coder/ToDoAppFastAPI/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/akihiro-coder/ToDoAppFastAPI/actions/workflows/ci.yml)

## 📝 概要

FastAPI + Docker + GitHub Actions を用いた学習用の ToDo アプリケーションです。  
認証（JWT）、認可、非同期API、DBスキーマ設計、CI、パフォーマンス最適化を実装し、実務レベルを意識して構築しています。

---

## ⚙️ 使用技術

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Auth**: OAuth2 Password Flow (JWT)
- **Test**: Pytest, pytest-asyncio, httpx
- **Infra**: Docker, GitHub Actions, Alembic
- **CI/CD**: 自動テスト、Lint実行
- **その他**: dotenv, Alembicマイグレーション

---

## ✅ 実装済み機能一覧

- [x] ユーザー登録・ログイン（JWT）
- [x] ToDo CRUD（ユーザーごとの認可処理）
- [x] 非同期APIテスト（pytest）
- [x] Docker コンテナ起動
- [x] GitHub Actions によるCI
- [x] Alembicマイグレーション管理
- [x] DBパフォーマンス改善（user_idインデックス追加）

---

## 🛠 技術的工夫点

- **スキーマ設計**：PydanticモデルとORMモデルを分離。明確な責務分離。
- **認証・認可**：JWTトークンによるログイン認証。ToDo操作には認可チェックを導入。
- **非同期テスト**：httpx.AsyncClient + pytest-asyncio による E2E 的なAPIテストを実施。
- **マイグレーション**：AlembicでDBスキーマを管理。user_id に index を付与してパフォーマンス改善。
- **CI導入**：GitHub Actions でテストとLintを自動実行。
- **環境変数管理**：`.env` ファイルと Docker 環境の連携。

---

## 🧪 テスト

`pytest` によるテストは以下をカバーしています：

- ToDoの作成 / 取得 / 更新 / 削除（認証あり・なし）
- 他ユーザーのToDoにアクセスしようとすると403
- 存在しないToDoにアクセスしようとすると404

テストコマンド：

```bash
PYTHONPATH=. pytest -v tests/test_todo.py
```

テスト結果は全てPASS（7件）

---

## 📑 API仕様

➡️ [こちらにまとめました](#api仕様)

---

## 🐳 起動方法（Docker）

### ✅ 前提条件

- Docker
- Docker Compose

### 🐳 起動コマンド

```bash
docker compose up --build
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### ⚙️ .envファイル

プロジェクトルート直下に `.env` を作成：

```dotenv
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 🛑 停止方法

```bash
docker compose down
```

---

## 🚀 パフォーマンス最適化

- `todos.user_id` にインデックスを追加（Alembic適用）
- ユーザーごとのデータ取得を高速化

---

## API仕様

### `GET /todos/todos` – Get My Todos

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| skip | integer | No | スキップする件数 |
| limit | integer | No | 取得件数の上限 |

#### レスポンス例

```json
[
  {
    "id": 1,
    "title": "買い物",
    "description": "牛乳を買う",
    "completed": false,
    "user_id": 1
  }
]
```

---

### `POST /todos/todos` – Create Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| title | string | Yes | タイトル |
| description | string | No | 説明 |
| completed | boolean | No | 完了フラグ |

#### レスポンス例

```json
{
  "id": 1,
  "title": "買い物",
  "description": "牛乳を買う",
  "completed": false,
  "user_id": 1
}
```

---

### `GET /todos/todos/{todo_id}` – Read Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id | integer | Yes | ToDo ID |

#### レスポンス例

```json
{
  "id": 1,
  "title": "買い物",
  "description": "牛乳を買う",
  "completed": false,
  "user_id": 1
}
```

---

### `PUT /todos/todos/{todo_id}` – Update Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id | integer | Yes | ToDo ID |
| title | string | Yes | タイトル |
| description | string | No | 説明 |
| completed | boolean | No | 完了フラグ |

#### レスポンス例

```json
{
  "id": 1,
  "title": "更新後",
  "description": "説明更新",
  "completed": true,
  "user_id": 1
}
```

---

### `DELETE /todos/todos/{todo_id}` – Delete Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id | integer | Yes | ToDo ID |

#### レスポンス例

- ステータスコード: `204 No Content`
- レスポンスボディなし

---

### `POST /users/signup` – Create User

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| email | string | Yes | メールアドレス |
| password | string | Yes | パスワード |

#### レスポンス例

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

---

### `POST /users/login` – Login

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| username | string | Yes | メールアドレス |
| password | string | Yes | パスワード |

#### レスポンス例

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

### `GET /users/me` – Read Current User

#### レスポンス例

```json
{
  "id": 1,
  "email": "user@example.com"
}
```