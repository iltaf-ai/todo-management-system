const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/login";
}

async function getTodos() {

    const response = await fetch("/todo", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
        return;
    }

    const todos = await response.json();

    const todoList = document.getElementById("todoList");

    todoList.innerHTML = "";

    if (todos.length === 0) {
        todoList.innerHTML = "<p>No todos found.</p>";
        return;
    }

    todos.forEach(todo => {

        const div = document.createElement("div");

        div.className = "todo-item";

        div.innerHTML = `
            <div>
                <h3>${todo.work}</h3>
                <p>
                    ${todo.completed ? "Completed" : "Pending"}
                </p>
            </div>

            <div>
                <button onclick="updateTodo(${todo.id})">
                    Update
                </button>

                <button onclick="deleteTodo(${todo.id})">
                    Delete
                </button>
            </div>
        `;

        todoList.appendChild(div);
    });
}

document.getElementById("todoForm").addEventListener(
    "submit",
    async function(e) {

        e.preventDefault();

        const work =
            document.getElementById("work").value;

        const completed =
            document.getElementById("completed").checked;

        const response = await fetch("/todo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                work: work,
                completed: completed
            })
        });

        const data = await response.json();

        document.getElementById("message").innerText =
            data.message;

        document.getElementById("work").value = "";
        document.getElementById("completed").checked = false;

        getTodos();
    }
);

async function updateTodo(todoId) {

    const newWork = prompt("Enter new task:");

    if (!newWork) {
        return;
    }

    const response = await fetch(`/todo/${todoId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            work: newWork,
            completed: false
        })
    });

    const data = await response.json();

    document.getElementById("message").innerText =
        data.message;

    getTodos();
}

async function deleteTodo(todoId) {

    const response = await fetch(`/todo/${todoId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    document.getElementById("message").innerText =
        data.message;

    getTodos();
}

document.getElementById("backBtn").addEventListener(
    "click",
    function() {
        window.location.href = "/dashboard";
    }
);

document.getElementById("logoutBtn").addEventListener(
    "click",
    function() {
        localStorage.removeItem("token");
        window.location.href = "/login";
    }
);

getTodos();