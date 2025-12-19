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
const tasksContainer = document.getElementById("tasks-container");
const addTaskBtn = document.getElementById("add-task-btn");

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
    openActionModal({
        title: "Create Workspace",
        bodyHTML: `
            <label>Workspace name</label>
            <input type="text" id="modal-workspace-name">
        `,
        onConfirm: async () => {
            const input = document.getElementById("modal-workspace-name");
            const name = input.value.trim();
            if (!name) return showAlert("Workspace name is required.");

            const res = await fetchJSON("/api/todo/workspace", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name }),
            });

            if (!res.success) {
                showAlert(res.error);
                return;
            }

            setCurrentWorkspace(name);
            await loadWorkspaces();
        }
    });
}


async function deleteWorkspace() {
    if (!currentWorkspace) return;

    openActionModal({
        title: "Delete Workspace",
        bodyHTML: `
            <p>Delete workspace <strong>${currentWorkspace}</strong>?</p>
            <p>This will remove all tasks.</p>
        `,
        onConfirm: async () => {
            const res = await fetchJSON(
                `/api/todo/workspace/${encodeURIComponent(currentWorkspace)}`,
                { method: "DELETE" }
            );

            if (!res.success) {
                showAlert(res.error);
                return;
            }

            currentWorkspace = null;
            await loadWorkspaces();
        }
    });
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

        deleteBtn.addEventListener("click", () => {
            openActionModal({
                title: "Delete Task",
                bodyHTML: `
                    <p>Delete task <strong>${task.title}</strong>?</p>
                    <p>This action cannot be undone.</p>
                `,
                onConfirm: async () => {
                    const res = await fetchJSON(
                        `/api/todo/tasks/${encodeURIComponent(currentWorkspace)}/${index}`,
                        { method: "DELETE" }
                    );

                    if (!res.success) {
                        showAlert(res.error);
                        return;
                    }

                    loadTasks();
                }
            });
        });
        btnContainer.appendChild(deleteBtn);
    });
}


function openCreateTaskModal() {
    if (!currentWorkspace) {
        showAlert("Select a workspace first.");
        return;
    }

    openTaskModal({ mode: "create" });
}

addTaskBtn.addEventListener("click", openCreateTaskModal);

// ==============================
// Create/Edit Task Modal
// ==============================

// References to modal elements
const editModal = document.getElementById("edit-task-modal");
const editTitleInput = document.getElementById("edit-task-title");
const editDescInput = document.getElementById("edit-task-desc");
const editSaveBtn = document.getElementById("save-edit");
const editCancelBtn = document.getElementById("cancel-edit");

// Open the modal with task data
let taskModalMode = "edit";
let currentEditIndex = null;

function openTaskModal({ mode, task = null, index = null }) {
    taskModalMode = mode;
    currentEditIndex = mode === "edit" ? index : null;

    editTitleInput.value = task ? task.title : "";
    editDescInput.value = task ? task.description : "";

    editModal.querySelector("h2").textContent =
        mode === "edit" ? "Edit Task" : "Create Task";

    editModal.classList.add("show");
}

// Close the modal
function closeModal() {
    currentEditIndex = null;
    taskModalMode = "edit";
    editModal.classList.remove("show");
}

function startEditTask(task, index) {
    openTaskModal({mode: "edit", task, index});
}

// Save changes
editSaveBtn.addEventListener("click", async () => {
    const title = editTitleInput.value.trim();
    const description = editDescInput.value.trim();

    if (!title) {
        showAlert("Task title is required.");
        return;
    }

    let res;

    if (taskModalMode === "edit") {
        // EDIT (PUT)
        res = await fetchJSON(
            `/api/todo/tasks/${encodeURIComponent(currentWorkspace)}/${currentEditIndex}`,
            {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, description }),
            }
        );
    } else {
        // CREATE (POST)
        res = await fetchJSON(
            `/api/todo/tasks/${encodeURIComponent(currentWorkspace)}`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, description }),
            }
        );
    }

    if (!res.success) {
        showAlert(res.error);
        return;
    }

    loadTasks();
    closeModal();
});

// Cancel editing
editCancelBtn.addEventListener("click", closeModal);


// ==============================
// Generic Action Modal
// ==============================

const actionModal = document.getElementById("action-modal");
const actionTitle = document.getElementById("action-modal-title");
const actionBody = document.getElementById("action-modal-body");
const actionConfirmBtn = document.getElementById("action-confirm");
const actionCancelBtn = document.getElementById("action-cancel");

let actionConfirmHandler = null;

function openActionModal({ title, bodyHTML, onConfirm }) {
    actionTitle.textContent = title;
    actionBody.innerHTML = bodyHTML;
    actionConfirmHandler = onConfirm;
    actionModal.classList.add("show");
}

function closeActionModal() {
    actionModal.classList.remove("show");
    actionBody.innerHTML = "";
    actionConfirmHandler = null;
}

actionConfirmBtn.addEventListener("click", async () => {
    if (actionConfirmHandler) await actionConfirmHandler();
    closeActionModal();
});

actionCancelBtn.addEventListener("click", closeActionModal);

// ==============================
// Initialize
// ==============================

loadWorkspaces();

