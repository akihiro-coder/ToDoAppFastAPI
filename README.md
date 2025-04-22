# ToDoアプリ（FastAPI）

[![CI](https://github.com/akihiro-coder/ToDoAppFastAPI/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/akihiro-coder/ToDoAppFastAPI/actions/workflows/ci.yml)

## 概要
FastAPI + Docker + GitHub Actions による学習用 ToDo アプリ。

# ToDoAppFastAPI
### スケジュール

| 日付 | 内容 | 対応スキル |
|------|------|------------|
| Day 1 | 認可処理（ToDoをユーザーに紐づける） | DB設計、認証・認可、SQLAlchemy |
| Day 2 | テスト導入（pytestによるユニット・統合テスト） | テスト実装経験、品質改善 |
| Day 3 | Docker化、`.env`による設定管理、ローカルDB分離 | DevOps基礎、チーム開発対応 |
| Day 4 | GitHub ActionsによるCI/CD導入 | CI/CD、継続的インテグレーション |
| Day 5 | ログ設計、Sentry導入、パフォーマンス改善 | モニタリング、最適化経験 |
| Day 6 | コード整備、README作成、デモ準備 | 設計力、説明力、成果物提示準備 |

---

### 実装予定機能一覧

- [x] ユーザー登録機能（/signup）
- [x] ログイン機能（JWT発行 / /login）
- [x] 認証付きユーザー情報取得（/me）
- [x] ToDoのユーザー紐付け（認可処理）
- [ ] pytestによるテスト実装
- [ ] Docker化（Dockerfile, docker-compose）
- [ ] `.env` による環境設定管理
- [ ] GitHub Actionsによる自動テスト導入
- [ ] Sentryによるエラーログ管理
- [ ] パフォーマンス改善（インデックス、クエリ最適化）
- [ ] README整備（構成図、API仕様、使用手順等）




## ✅ テストケース一覧（認証・認可付きToDoアプリ）

### 🎯 テスト対象機能
- サインアップ（ユーザー作成）
- ログイン（JWT取得）
- ToDoの作成（認証ユーザーのみ）
- ToDoの一覧取得（自分のToDoのみ取得）
- 他ユーザーとのToDoの分離（認可）
- JWTトークンの使用と未使用による制御

---

### 🧪 テストケース一覧
#### ✅ 認可付きToDo操作（一覧取得 / 作成）のテストケース

| No | シナリオ | 操作 | 期待される結果 |
|----|----------|------|----------------|
| 1 | ユーザーAを新規登録 | `/signup` にPOST | ステータス200、ユーザー作成成功 |
| 2 | ユーザーAでログイン | `/login` にPOST | アクセストークンが返ってくる |
| 3 | ユーザーAでToDoを作成 | `/todos` にPOST（トークン付き） | ステータス200、ToDo作成成功・user_idがAのID |
| 4 | ユーザーAでToDo一覧を取得 | `/todos` にGET（トークン付き） | ユーザーAのToDoのみが表示される |
| 5 | ユーザーBを新規登録 | `/signup` にPOST | ステータス200、ユーザーB作成成功 |
| 6 | ユーザーBでログイン | `/login` にPOST | Bのアクセストークンが返ってくる |
| 7 | ユーザーBでToDo一覧を取得 | `/todos` にGET（Bのトークン付き） | ユーザーBのToDoは0件（ユーザーAのToDoは見えない） |
| 8 | 認証なしでToDo一覧を取得 | `/todos` にGET（トークンなし） | ステータス401（Unauthorized） |
| 9 | 認証なしでToDo作成 | `/todos` にPOST（トークンなし） | ステータス401（Unauthorized） |






#### ✅ 認可付きToDo操作（詳細取得 / 更新 / 削除）のテストケース

| No | シナリオ | 操作 | 期待される結果 |
|----|----------|------|----------------|
| 1 | ユーザーAがToDoを作成 | `/todos` にPOST（Aで認証） | ステータス200、ToDo作成成功（id=1など） |
| 2 | ユーザーAが自分のToDoを詳細取得 | `GET /todos/1`（Aで認証） | ステータス200、該当ToDoが返る |
| 3 | ユーザーAが自分のToDoを更新 | `PUT /todos/1`（Aで認証） | ステータス200、内容が更新される |
| 4 | ユーザーAが自分のToDoを削除 | `DELETE /todos/1`（Aで認証） | ステータス200、削除成功メッセージ |
| 5 | ユーザーBがユーザーAのToDoを詳細取得 | `GET /todos/1`（Bで認証） | ステータス403、認可エラー |
| 6 | ユーザーBがユーザーAのToDoを更新 | `PUT /todos/1`（Bで認証） | ステータス403、認可エラー |
| 7 | ユーザーBがユーザーAのToDoを削除 | `DELETE /todos/1`（Bで認証） | ステータス403、認可エラー |
| 8 | 存在しないToDoを取得 | `GET /todos/999`（任意ユーザー） | ステータス404、Not Found |
| 9 | 存在しないToDoを更新 | `PUT /todos/999`（任意ユーザー） | ステータス404、Not Found |
|10 | 存在しないToDoを削除 | `DELETE /todos/999`（任意ユーザー） | ステータス404、Not Found |



### ✅ 認証・認可の動作確認結果

- JWTがないと `/todos` にアクセス不可（401）
- 一覧取得では、自分のToDoのみ表示される（他人のToDoは見えない）
- 作成時に `user_id` が自動で紐づけられる
- 更新では、自分のToDoのみを更新できる
- 削除では、自分のToDoのみを削除できる

---



## 🧪 自動テストの実装

このアプリケーションでは、**FastAPI + pytest + httpx.AsyncClient** を用いた自動テストを導入しています。

### ✅ 使用技術

- `pytest`：テストフレームワーク
- `pytest-asyncio`：非同期テスト対応
- `httpx.AsyncClient` + `ASGITransport`：FastAPIの `TestClient` より実践的な非同期APIクライアント
- `PYTHONPATH=.` によるパス解決（`app.main` のimport）

---

### ✅ テスト対象API一覧

| メソッド | エンドポイント | テスト内容 |
|----------|----------------|------------|
| POST     | `/todos/todos`        | ToDo作成（正常系、未認証＝401） |
| GET      | `/todos/todos`        | ToDo一覧取得（正常系） |
| GET      | `/todos/todos/{id}`   | ToDo詳細取得（正常系、存在しないID＝404） |
| PUT      | `/todos/todos/{id}`   | ToDo更新（正常系、他人のデータ更新＝403） |
| DELETE   | `/todos/todos/{id}`   | ToDo削除（正常系、削除後に404を確認） |

---

### ✅ テスト設計ポリシー

- 各テスト関数は **完全に自己完結型**  
  （ユーザー登録 → ログイン → トークン取得 → 処理 の一連を含む）
- CRUDの正常系だけでなく、**異常系（401, 403, 404）も明確にカバー**
- 各API操作に対して、**HTTPステータスコード・レスポンスの整合性を検証**
- `@pytest.mark.asyncio` を先頭に定義し、すべてのテストを非同期で統一
- DB汚染を避けるため、各テストで個別ユーザー／データを使用

---

### ✅ テスト実行方法

以下のコマンドを使用して、すべてのテストが実行されます：

```bash
PYTHONPATH=. pytest -v tests/test_todo.py
```


=============================== test session starts ================================
platform linux -- Python 3.12.3, pytest-8.3.5
collected 7 items

tests/test_todo.py::test_create_todo_success PASSED                         [ 14%]
tests/test_todo.py::test_read_todo_success   PASSED                         [ 28%]
tests/test_todo.py::test_update_todo_success PASSED                         [ 42%]
tests/test_todo.py::test_delete_todo_success PASSED                         [ 57%]
tests/test_todo.py::test_create_todo_unauthorized PASSED                    [ 71%]
tests/test_todo.py::test_update_todo_forbidden PASSED                       [ 85%]
tests/test_todo.py::test_get_todo_not_found PASSED                          [100%]

=============================== 7 passed in 1.77s ===============================



## 🚀 起動方法（Docker利用）

このアプリケーションは、**FastAPI + SQLite** で構成されており、Dockerを使用して簡単にローカル実行できます。

### ✅ 前提条件

- Docker
- Docker Compose

---

### 🐳 起動コマンド

プロジェクトルートにて、以下を実行してください：

```bash
docker compose up --build
```

---

### 🌍 アクセス確認
起動後、以下のURLにアクセスすることで、Swagger UI（APIドキュメント）を確認できます：

📎 http://localhost:8000/docs

---

### ⚙️ .envファイルについて
アプリケーションの設定値は .env ファイルに定義されています。
プロジェクトルート直下に以下のような内容で .env を作成してください：

```.dotenv
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
※ docker-compose.yml でこのファイルを読み込むように設定されています。

---

### 🛑 停止方法
アプリケーションの起動を終了したい場合は、以下のコマンドを実行します：

```bash
docker compose down
```


---
## API仕様

### `GET /todos/todos`
- Get My Todos

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| skip (query) | integer | No | スキップする件数 |
| limit (query) | integer | No | 取得件数の上限 |

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

### `POST /todos/todos`
- Create Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| title (body) | string | Yes | ToDoのタイトル |
| description (body) | string | No | ToDoの説明 |
| completed (body) | boolean | No | 完了済みかどうかのフラグ |

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

### `GET /todos/todos/{todo_id}`
- Read Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id (path) | integer | Yes | ToDoのID |

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

### `PUT /todos/todos/{todo_id}`
- Update Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id (path) | integer | Yes | ToDoのID |
| title (body) | string | Yes | ToDoのタイトル |
| description (body) | string | No | ToDoの説明 |
| completed (body) | boolean | No | 完了済みかどうかのフラグ |

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

### `DELETE /todos/todos/{todo_id}`
- Delete Todo

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| todo_id (path) | integer | Yes | ToDoのID |

#### レスポンス例
```json
{
  "message": "削除しました。"
}
```

### `POST /users/signup`
- Create User

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| email (body) | string | Yes | ユーザーのメールアドレス |
| password (body) | string | Yes | パスワード |

#### レスポンス例
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### `POST /users/login`
- Login

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|------|------|
| grant_type (body) | string | No | パラメータ |
| username (body) | string | Yes | パラメータ |
| password (body) | string | Yes | パスワード |
| scope (body) | string | No | パラメータ |
| client_id (body) | string | No | クライアントID |
| client_secret (body) | string | No | パラメータ |

#### レスポンス例
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### `GET /users/me`
- Read Current User

#### レスポンス例
```json
{
  "id": 1,
  "email": "user@example.com"
}
```