# backend/todo/routes.py

"""
To-Do List Routes
-----------------
Provides RESTful API endpoints for workspaces and tasks.
All routes return JSON responses with success/error messages.
"""

from flask import Blueprint, request, jsonify
from backend.todo import service

todo_bp = Blueprint("todo", __name__, url_prefix="/api/todo")

# -----------------------------
# Workspace Endpoints
# -----------------------------

@todo_bp.route("/workspaces", methods=["GET"])
def get_workspaces():
    """Return a list of all workspace names."""
    try:
        workspaces = service.get_workspaces()
        return jsonify({"success": True, "workspaces": workspaces})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@todo_bp.route("/workspace", methods=["POST"])
def add_workspace():
    """Add a new workspace."""
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"success": False, "error": "Workspace name is required"}), 400
    try:
        service.add_workspace(name)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@todo_bp.route("/workspace/<name>", methods=["DELETE"])
def remove_workspace(name):
    """Remove a workspace."""
    try:
        service.remove_workspace(name)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -----------------------------
# Task Endpoints
# -----------------------------

@todo_bp.route("/tasks/<workspace>", methods=["GET"])
def get_tasks(workspace):
    """Return all tasks from a workspace."""
    try:
        tasks = service.get_tasks(workspace)
        return jsonify({"success": True, "tasks": tasks})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@todo_bp.route("/tasks/<workspace>", methods=["POST"])
def add_task(workspace):
    """Add a task to a workspace."""
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    if not title:
        return jsonify({"success": False, "error": "Task title is required"}), 400
    try:
        service.add_task(workspace, title, description)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@todo_bp.route("/tasks/<workspace>/<int:index>", methods=["DELETE"])
def remove_task(workspace, index):
    """Remove a task by index from a workspace."""
    try:
        service.remove_task(workspace, index)
        return jsonify({"success": True})
    except (ValueError, IndexError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@todo_bp.route("/tasks/<workspace>/<int:index>", methods=["PUT"])
def api_edit_task(workspace, index):
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        service.edit_task(workspace, index, title, description)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
