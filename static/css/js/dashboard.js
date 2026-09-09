const token = localStorage.getItem("token");


// Login nahi hai
if (!token) {
    window.location.href = "/login";
}


// GET TODOS
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

    // Agar backend .all() return karega
    todos.forEach(todo => {

        const div = document.createElement("div");

        div.innerHTML = `
            <p>
                ${todo.work}
                ${todo.completed ? "✅" : "❌"}
            </p>

            <button onclick="updateTodo(${todo.id})">
                Update
            </button>

            <button onclick="deleteTodo(${todo.id})">
                Delete
            </button>
        `;

        todoList.appendChild(div);
    });
}


// ADD TODO
document.getElementById("todoForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    const work = document.getElementById("work").value;
    const completed = document.getElementById("completed").checked;

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

    document.getElementById("message").innerText = data.message;

    document.getElementById("work").value = "";
    document.getElementById("completed").checked = false;

    getTodos();
});


// UPDATE TODO
async function updateTodo(todoId) {

    const newWork = prompt("Enter new work:");

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

    document.getElementById("message").innerText = data.message;

    getTodos();
}


// DELETE TODO
async function deleteTodo(todoId) {

    const response = await fetch(`/todo/${todoId}`, {

        method: "DELETE",

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    document.getElementById("message").innerText = data.message;

    getTodos();
}


// LOGOUT
document.getElementById("logoutBtn").addEventListener("click", function() {

    localStorage.removeItem("token");

    window.location.href = "/login";
});


// Page open hote hi todos load
getTodos();