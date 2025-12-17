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
