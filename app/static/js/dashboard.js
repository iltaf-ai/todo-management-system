const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/login";
}

document.getElementById("todoBtn").addEventListener(
    "click",
    function () {
        window.location.href = "/todo-page";
    }
);

document.getElementById("logoutBtn").addEventListener(
    "click",
    function () {
        localStorage.removeItem("token");
        window.location.href = "/login";
    }
);