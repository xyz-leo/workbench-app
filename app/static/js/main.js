// =============================
// Theme handling (dark / light)
// =============================

(function () {
    const THEME_KEY = "workbench_theme";
    const root = document.documentElement;
    const toggleButton = document.getElementById("theme-toggle");

    function applyTheme(theme) {
        root.setAttribute("data-theme", theme);
        toggleButton.textContent = theme === "dark" ? "☾" : "☀";
    }

    function getSavedTheme() {
        return localStorage.getItem(THEME_KEY);
    }

    function saveTheme(theme) {
        localStorage.setItem(THEME_KEY, theme);
    }

    function toggleTheme() {
        const currentTheme = root.getAttribute("data-theme") || "dark";
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        applyTheme(newTheme);
        saveTheme(newTheme);
    }

    // Initial load
    const savedTheme = getSavedTheme();
    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        applyTheme("dark");
        saveTheme("dark");
    }

    // Events
    if (toggleButton) {
        toggleButton.addEventListener("click", toggleTheme);
    }
})();

// Shutdown server button
document.getElementById("shutdown-btn").addEventListener("click", () => {
    const msg = document.createElement("div");
    msg.textContent = "Application closed. You may now close this tab.";
    msg.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #111;
        color: #10a37f;
        padding: 20px;
        text-align: center;
        z-index: 9999;
        font-family: sans-serif;
        font-size: 22px;
    `;
    document.body.appendChild(msg);

    fetch("/shutdown", { method: "POST" });
});
