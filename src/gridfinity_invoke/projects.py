"""Project management module for Gridfinity projects.

Handles active project state, project configuration, and component management.
"""

import json
from pathlib import Path

# Project storage directories
PROJECTS_DIR = Path("projects")
ACTIVE_FILE = Path(".gridfinity-active")


def get_active_project() -> str | None:
    """Get the currently active project name.

    Returns:
        Project name if active project exists, None otherwise.
    """
    try:
        return ACTIVE_FILE.read_text().strip()
    except FileNotFoundError:
        return None


def set_active_project(name: str) -> None:
    """Set the active project.

    Args:
        name: Project name to set as active.
    """
    ACTIVE_FILE.write_text(name)


def get_project_path(name: str) -> Path:
    """Get the path to a project directory.

    Args:
        name: Project name.

    Returns:
        Path to the project directory (projects/<name>/).
    """
    return PROJECTS_DIR / name


def load_project_config(name: str) -> dict:
    """Load and parse a project's configuration.

    Args:
        name: Project name.

    Returns:
        Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the project or config doesn't exist.
        json.JSONDecodeError: If the config is invalid JSON.
    """
    config_path = get_project_path(name) / "config.json"
    return json.loads(config_path.read_text())


def save_project_config(name: str, config: dict) -> None:
    """Save a project configuration to disk.

    Args:
        name: Project name.
        config: Configuration dictionary to save.
    """
    project_path = get_project_path(name)
    project_path.mkdir(parents=True, exist_ok=True)

    config_path = project_path / "config.json"
    config_path.write_text(json.dumps(config, indent=2))


def add_component_to_config(name: str, component: dict) -> None:
    """Add or update a component in the project configuration.

    If a component with the same name already exists, it is replaced.
    Otherwise, the new component is appended.

    Args:
        name: Project name.
        component: Component dictionary with at minimum a 'name' key.
    """
    config = load_project_config(name)

    # Find and update existing component or add new one
    component_name = component["name"]
    components = config["components"]

    # Check for existing component with same name
    for i, existing in enumerate(components):
        if existing["name"] == component_name:
            components[i] = component
            save_project_config(name, config)
            return

    # No duplicate found, append new component
    components.append(component)
    save_project_config(name, config)
