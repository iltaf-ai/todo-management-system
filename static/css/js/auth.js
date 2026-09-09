// Register

document.getElementById("registerForm")?.addEventListener("submit", async function(e) {

    e.preventDefault();

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    });

    const data = await response.json();

    document.getElementById("message").innerText = data.message;

    if (response.ok && data.message === "User registered successfully") {
        window.location.href = "/login";
    }
});


// Login

document.getElementById("loginForm")?.addEventListener("submit", async function(e) {

    e.preventDefault();

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    });

    const data = await response.json();

    if (response.ok && data.token) {

        localStorage.setItem("token", data.token);

        window.location.href = "/dashboard";
    } 
    else {
        document.getElementById("message").innerText = data.message;
    }
});