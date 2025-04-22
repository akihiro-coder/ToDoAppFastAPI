document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById("login-form");
    const todosList = document.getElementById("todos");


    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = loginForm.email.value;
        const password = loginForm.password.value;

        try {
            // 1. ログインAPIにPOST
            const res = await fetch("/users/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    username: email,
                    password: password,
                }),
                cache: "no-store"
            });
        },

        if (!res.ok) {
            alert("ログインに失敗しました");
            return;
        }

        const data = await res.json();
        const token = data.access_token;
        localStorage.setItem("access_token", token); // トークン保存


        // 2. ToDo一覧取得
        const todosRes = await fetch("/todos/todos", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        const todos = await todosRes.json();
        todosList.innerHTML = ""; // 既存のToDoをクリア
        todos.forEach((todo) => {
            const li = document.createElement("li");
            li.textContent = `${todo.title} - ${todo.description || ""}`;
            todosList.appendChild(li);
        });

        catch (err) {
                console.error(err);
                alert("通信エラー");
            }
    });
});