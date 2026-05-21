function logout() {
    // 1. Target the logout button element if it exists to display a loading state
    const logoutBtn = document.querySelector('button[onclick="logout()"]') || document.activeElement;
    const originalText = logoutBtn ? logoutBtn.innerText : "Logout";
    
    if (logoutBtn && logoutBtn.tagName === "BUTTON") {
        logoutBtn.disabled = true;
        logoutBtn.innerText = "Processing...";
    }

    // 2. Transmit the payload to the storage core system
    fetch("/api/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({}) // Fixed: passing empty object instead of blank arguments
    })
    .then(response => {
        if (!response.ok) throw new Error("Logout request failed");
        return response.json();
    })
    .then(data => {
        // 3. Fire a beautiful confirmation message right before clean routing redirection
        if (typeof triggerToast === "function") {
            triggerToast("Session terminated. Redirecting to auth gateway...", "info");
        }
        
        setTimeout(() => {
            window.location.href = data["data"]; // Safely performs redirect operation
        }, 800);
    })
    .catch(err => {
        console.error("Session destruction error:", err);
        if (typeof triggerToast === "function") {
            triggerToast("Error clear token space. Forcing exit...", "error");
        }
        // Fallback redirection to home/login if api fails
        setTimeout(() => { window.location.href = "/login"; }, 1500);
    });
}