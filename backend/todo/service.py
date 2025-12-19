# backend/todo/service.py

"""
Business logic for the To-Do app.
Operates on workspaces and tasks using storage.py.
"""

from backend.todo.storage import load_data, save_data

# -----------------------------
# Workspaces
# -----------------------------

def get_workspaces():
    """Return a list of all workspace names."""
    data = load_data()
    return list(data.keys())

def add_workspace(name: str):
    """Add a new workspace."""
    data = load_data()
    if name in data:
        raise ValueError("Workspace already exists")
    data[name] = []
    save_data(data)

def remove_workspace(name: str):
    """Remove an existing workspace."""
    data = load_data()
    if name not in data:
        raise ValueError("Workspace does not exist")
    del data[name]
    save_data(data)

# -----------------------------
# Tasks
# -----------------------------

def get_tasks(workspace: str):
    """Return tasks in a workspace."""
    data = load_data()
    if workspace not in data:
        raise ValueError("Workspace does not exist")
    return data[workspace]

def add_task(workspace: str, title: str, description: str = ""):
    """Add a task to a workspace."""
    data = load_data()
    if workspace not in data:
        raise ValueError("Workspace does not exist")
    data[workspace].append({"title": title, "description": description})
    save_data(data)

def remove_task(workspace: str, index: int):
    """Remove a task by index from a workspace."""
    data = load_data()
    if workspace not in data:
        raise ValueError("Workspace does not exist")
    try:
        del data[workspace][index]
    except IndexError:
        raise IndexError("Task index out of range")
    save_data(data)

def edit_task(workspace: str, index: int, title: str = None, description: str = None):
    """Edit the title and/or description of a task."""
    data = load_data()
    if workspace not in data:
        raise ValueError("Workspace does not exist")
    try:
        task = data[workspace][index]
    except IndexError:
        raise IndexError("Task index out of range")
    
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description

    data[workspace][index] = task
    save_data(data)

