// Auto-dismiss flash alerts after 4 seconds for a cleaner UX.
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".alert").forEach(function (alertEl) {
        setTimeout(function () {
            const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
            if (alert) alert.close();
        }, 4000);
    });
});

// Dark mode toggle — theme is applied early (see base.html <head>) to
// avoid a flash of the wrong theme; this just wires up the button.
document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("themeToggleBtn");
    const icon = document.getElementById("themeIcon");
    const html = document.documentElement;

    function updateIcon() {
        const theme = html.getAttribute("data-bs-theme");
        icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
    }
    updateIcon();

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            const current = html.getAttribute("data-bs-theme");
            const next = current === "dark" ? "light" : "dark";
            html.setAttribute("data-bs-theme", next);
            localStorage.setItem("theme", next);
            updateIcon();
        });
    }
});