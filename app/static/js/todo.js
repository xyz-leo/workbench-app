// =============================
// todo.js (JSON in-memory)
// =============================

// All operations are done on a single in-memory object "todoData",

// -----------------------------
// JSON-like Storage (to delete later)
// -----------------------------
let todoData = {
    "Default Workspace": [] // Initial default workspace
};

// -----------------------------
// DOM Elements
// -----------------------------
const workspaceSelector = document.getElementById("workspace-selector");
const addWorkspaceBtn = document.getElementById("add-workspace");
const removeWorkspaceBtn = document.getElementById("remove-workspace");
const addTaskForm = document.getElementById("add-task-form");
const tasksContainer = document.getElementById("tasks-container");

// -----------------------------
// Utility Functions
// -----------------------------

// Get currently selected workspace
function getCurrentWorkspace() {
    return workspaceSelector.value;
}

// Render workspaces in the dropdown
function renderWorkspaces() {
    workspaceSelector.innerHTML = "";
    for (const workspace of Object.keys(todoData)) {
        const option = document.createElement("option");
        option.value = workspace;
        option.textContent = workspace;
        workspaceSelector.appendChild(option);
    }
}

// Render tasks for the selected workspace
function renderTasks() {
    const workspace = getCurrentWorkspace();
    const tasks = todoData[workspace] || [];

    tasksContainer.innerHTML = ""; // Clear previous tasks

    if (tasks.length === 0) {
        const emptyMsg = document.createElement("p");
        emptyMsg.textContent = "No tasks yet.";
        tasksContainer.appendChild(emptyMsg);
        return;
    }

    // Render each task as <details>
    tasks.forEach((task, index) => {
        const taskDetails = document.createElement("details");
        taskDetails.className = "panel";
        taskDetails.style.marginBottom = "0.5rem";

        // Summary = task title
        const summary = document.createElement("summary");
        summary.textContent = task.title;
        taskDetails.appendChild(summary);

        // Description
        if (task.description) {
            const descEl = document.createElement("p");
            descEl.style.marginTop = "0.5rem";
            descEl.textContent = task.description;
            taskDetails.appendChild(descEl);
        }

        // Delete task button
        const deleteBtn = document.createElement("button");
        deleteBtn.className = "button";
        deleteBtn.style.marginTop = "0.5rem";
        deleteBtn.textContent = "Delete";
        deleteBtn.onclick = () => {
            if (confirm(`Are you sure you want to delete task "${task.title}"?`)) {
                todoData[workspace].splice(index, 1);
                renderTasks();
            }
        };

        taskDetails.appendChild(deleteBtn);

        tasksContainer.appendChild(taskDetails);
    });
}

// -----------------------------
// Event Handlers
// -----------------------------

// Add new task
addTaskForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-desc").value.trim();
    const workspace = getCurrentWorkspace();

    if (!title) return;

    const task = { title, description };
    todoData[workspace].push(task);

    renderTasks();

    // Reset form
    addTaskForm.reset();
});

// Add new workspace
addWorkspaceBtn.addEventListener("click", () => {
    const workspaceName = prompt("Enter new workspace name:");
    if (!workspaceName) return;

    if (todoData[workspaceName]) {
        alert("Workspace already exists!");
        return;
    }

    todoData[workspaceName] = [];
    renderWorkspaces();
    workspaceSelector.value = workspaceName;
    renderTasks();
});

// Remove current workspace
removeWorkspaceBtn.addEventListener("click", () => {
    const workspace = getCurrentWorkspace();
    if (!workspace) return;

    if (!confirm(`Are you sure you want to delete workspace "${workspace}"?`)) return;

    delete todoData[workspace];
    renderWorkspaces();
    // Select first workspace if exists
    const first = Object.keys(todoData)[0];
    if (first) workspaceSelector.value = first;

    renderTasks();
});

// Switch workspace
workspaceSelector.addEventListener("change", renderTasks);

// -----------------------------
// Initial Render
// -----------------------------
renderWorkspaces();
renderTasks();

