// Auto-dismiss flash alerts after 4 seconds for a cleaner UX.
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".alert").forEach(function (alertEl) {
        setTimeout(function () {
            const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
            if (alert) alert.close();
        }, 4000);
    });
});
