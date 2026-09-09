// ==========================
// Get JWT Token
// ==========================

const token = localStorage.getItem("token");


// Agar token nahi hai
if (!token) {
    window.location.href = "/login";
}


// ==========================
// GET TODOS
// ==========================

async function getTodos() {

    const response = await fetch("/todo", {
        method: "GET",

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });


    // Token invalid / expired
    if (response.status === 401) {

        localStorage.removeItem("token");

        window.location.href = "/login";

        return;
    }


    const todos = await response.json();

    const todoList = document.getElementById("todoList");

    todoList.innerHTML = "";


    // Agar koi todo nahi
    if (todos.length === 0) {

        todoList.innerHTML = "<p>No todos found.</p>";

        return;
    }


    // Har todo ko show karo
    todos.forEach(todo => {

        const div = document.createElement("div");

        div.innerHTML = `
            <div class="todo-item">

                <p>
                    <strong>${todo.work}</strong>
                </p>

                <p>
                    Status:
                    ${todo.completed ? "✅ Completed" : "❌ Not Completed"}
                </p>

                <button onclick="updateTodo(${todo.id})">
                    Update
                </button>

                <button onclick="deleteTodo(${todo.id})">
                    Delete
                </button>

            </div>

            <hr>
        `;

        todoList.appendChild(div);
    });
}



// ==========================
// CREATE TODO
// ==========================

document
    .getElementById("todoForm")
    .addEventListener("submit", async function(e) {

        e.preventDefault();


        const work = document.getElementById("work").value;

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


        // Form clear
        document.getElementById("work").value = "";

        document.getElementById("completed").checked = false;


        // Todos dobara load
        getTodos();

    });



// ==========================
// UPDATE TODO
// ==========================

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


    document.getElementById("message").innerText =
        data.message;


    // Updated todos show karo
    getTodos();
}



// ==========================
// DELETE TODO
// ==========================

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


    // Todo list refresh
    getTodos();
}



// ==========================
// LOGOUT
// ==========================

document
    .getElementById("logoutBtn")
    .addEventListener("click", function() {

        localStorage.removeItem("token");

        window.location.href = "/login";

    });



// ==========================
// Load Todos When Page Opens
// ==========================

getTodos();