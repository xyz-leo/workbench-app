// static/js/todo.js

// ==============================
// In-memory state (mirrors backend)
// ==============================
let currentWorkspace = null;
let workspaces = [];

// ==============================
// DOM elements
// ==============================
const workspaceSelect = document.getElementById("workspace-selector");
const workspaceAddBtn = document.getElementById("add-workspace");
const workspaceDeleteBtn = document.getElementById("remove-workspace");
const addTaskForm = document.getElementById("add-task-form");
const taskTitleInput = document.getElementById("task-title");
const taskDescriptionInput = document.getElementById("task-desc");
const tasksContainer = document.getElementById("tasks-container");

// ==============================
// Helpers
// ==============================
async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    return res.json();
}

function showAlert(message) {
    alert(message);
}

// ==============================
// Workspace Functions
// ==============================

async function loadWorkspaces() {
    const res = await fetchJSON("/api/todo/workspaces");
    if (res.success) {
        workspaces = res.workspaces;

        // Recupera último workspace do localStorage
        const last = localStorage.getItem("lastWorkspace");
        if (last && workspaces.includes(last)) {
            currentWorkspace = last;
        } else {
            currentWorkspace = workspaces[0] || null;
        }

        renderWorkspaceSelect();
        if (currentWorkspace) await loadTasks();
    } else {
        showAlert(res.error);
    }
}


function renderWorkspaceSelect() {
    workspaceSelect.innerHTML = "";
    workspaces.forEach(ws => {
        const option = document.createElement("option");
        option.value = ws;
        option.textContent = ws;
        workspaceSelect.appendChild(option);
    });
    // Forces select to show the current workspace
    workspaceSelect.value = currentWorkspace;
}


async function addWorkspace() {
    const name = prompt("Enter new workspace name:");
    if (!name) return;

    const res = await fetchJSON("/api/todo/workspace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
    });

    if (res.success) {
        // Atualiza currentWorkspace e localStorage imediatamente
        setCurrentWorkspace(name);

        // Recarrega os workspaces
        await loadWorkspaces();
        await loadTasks();
    } else {
        showAlert(res.error);
    }
}


async function deleteWorkspace() {
    if (!currentWorkspace) return;
    if (!confirm(`Delete workspace "${currentWorkspace}"? This will remove all tasks.`)) return;

    const res = await fetchJSON(`/api/todo/workspace/${encodeURIComponent(currentWorkspace)}`, {
        method: "DELETE",
    });

    if (res.success) {
        currentWorkspace = workspaces.find(w => w !== currentWorkspace) || null;
        await loadWorkspaces();
    } else {
        showAlert(res.error);
    }
}

function setCurrentWorkspace(workspace) {
    currentWorkspace = workspace;
    workspaceSelect.value = workspace;
    localStorage.setItem("lastWorkspace", workspace); // saves in browser localstorage
}

workspaceSelect.addEventListener("change", async () => {
    setCurrentWorkspace(workspaceSelect.value);
    await loadTasks();
});

workspaceAddBtn.addEventListener("click", addWorkspace);
workspaceDeleteBtn.addEventListener("click", deleteWorkspace);

// ==============================
// Task Functions
// ==============================

async function loadTasks() {
    tasksContainer.innerHTML = "";
    if (!currentWorkspace) return;

    const res = await fetchJSON(`/api/todo/tasks/${encodeURIComponent(currentWorkspace)}`);
    if (!res.success) {
        showAlert(res.error);
        return;
    }

    res.tasks.forEach((task, index) => {
        const details = document.createElement("details");
        const summary = document.createElement("summary");
        details.className = "panel";
        details.style.marginBottom = "0.5rem";
        summary.textContent = task.title;
        details.appendChild(summary);

        // Description paragraph
        const description = document.createElement("p");
        description.textContent = task.description;
        details.appendChild(description);

        // Buttons container
        const btnContainer = document.createElement("div");
        btnContainer.style.marginTop = "0.5rem";
        details.appendChild(btnContainer);
  
        // Edit button
        const editBtn = document.createElement("button");
        editBtn.className = "button";
        editBtn.style.marginRight = "0.5rem";
        editBtn.textContent = "Edit";
        editBtn.addEventListener("click", () => startEditTask(task, index));
        btnContainer.appendChild(editBtn);

        tasksContainer.appendChild(details);

        // Delete button
        const deleteBtn = document.createElement("button");
        deleteBtn.className = "button";
        deleteBtn.textContent = "Delete";
        deleteBtn.addEventListener("click", async () => {
            if (!confirm(`Delete task "${task.title}"?`)) return;
            const delRes = await fetchJSON(`/api/todo/tasks/${encodeURIComponent(currentWorkspace)}/${index}`, {
                method: "DELETE",
            });
            if (delRes.success) loadTasks();
            else showAlert(delRes.error);
        });

        btnContainer.appendChild(deleteBtn);
    });
}


async function addTask(event) {
    event.preventDefault();
    if (!currentWorkspace) {
        showAlert("Select a workspace first.");
        return;
    }

    const title = taskTitleInput.value.trim();
    const description = taskDescriptionInput.value.trim();

    if (!title) {
        showAlert("Task title is required.");
        return;
    }

    const res = await fetchJSON(`/api/todo/tasks/${encodeURIComponent(currentWorkspace)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description }),
    });

    if (res.success) {
        taskTitleInput.value = "";
        taskDescriptionInput.value = "";
        loadTasks();
    } else {
        showAlert(res.error);
    }
}

addTaskForm.addEventListener("submit", addTask);

// ==============================
// Edit Task Modal
// ==============================

// References to modal elements
const editModal = document.getElementById("edit-task-modal");
const editTitleInput = document.getElementById("edit-task-title");
const editDescInput = document.getElementById("edit-task-desc");
const editSaveBtn = document.getElementById("save-edit");
const editCancelBtn = document.getElementById("cancel-edit");

let currentEditIndex = null;

// Open the modal with task data
function openModal(task, index) {
    currentEditIndex = index;
    editTitleInput.value = task.title;
    editDescInput.value = task.description;
    editModal.classList.add("show"); // use CSS show class
}

// Close the modal
function closeModal() {
    currentEditIndex = null;
    editModal.classList.remove("show");
}

// Replace old startEditTask function
function startEditTask(task, index) {
    openModal(task, index);
}

// Save changes
editSaveBtn.addEventListener("click", async () => {
    const newTitle = editTitleInput.value.trim();
    const newDescription = editDescInput.value.trim();

    if (!newTitle) {
        showAlert("Task title is required.");
        return;
    }

    const res = await fetchJSON(`/api/todo/tasks/${encodeURIComponent(currentWorkspace)}/${currentEditIndex}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, description: newDescription }),
    });

    if (res.success) {
        loadTasks();
        closeModal();
    } else {
        showAlert(res.error);
    }
});

// Cancel editing
editCancelBtn.addEventListener("click", closeModal);

// ==============================
// Initialize
// ==============================

loadWorkspaces();

