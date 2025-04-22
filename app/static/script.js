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
        const todosRes = await fetch("/todos/")

    })
})