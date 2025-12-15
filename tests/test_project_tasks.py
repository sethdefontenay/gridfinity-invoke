"""Tests for project management invoke tasks."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from invoke import MockContext

from gridfinity_invoke import projects


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        projects_dir = tmpdir_path / "projects"
        with patch.object(projects, "PROJECTS_DIR", projects_dir):
            with patch.object(projects, "ACTIVE_FILE", active_file):
                yield tmpdir_path


def test_new_project_creates_directory_and_config(temp_project_dir: Path) -> None:
    """Test new-project creates directory and config.json with correct structure."""
    from invoke_collections.gf import new_project

    ctx = MockContext()
    project_name = "test-project"

    new_project(ctx, name=project_name)

    # Verify directory was created
    project_dir = temp_project_dir / "projects" / project_name
    assert project_dir.exists()
    assert project_dir.is_dir()

    # Verify config.json was created with correct structure
    config_file = project_dir / "config.json"
    assert config_file.exists()

    config = json.loads(config_file.read_text())
    assert config["name"] == project_name
    assert config["components"] == []


def test_new_project_sets_project_as_active(temp_project_dir: Path) -> None:
    """Test new-project sets the newly created project as active."""
    from invoke_collections.gf import new_project

    ctx = MockContext()
    project_name = "active-test-project"

    new_project(ctx, name=project_name)

    # Verify project is now active
    active_project = projects.get_active_project()
    assert active_project == project_name


def test_new_project_fails_if_project_exists(temp_project_dir: Path) -> None:
    """Test new-project fails with error if project already exists."""
    from invoke_collections.gf import new_project

    ctx = MockContext()
    project_name = "duplicate-project"

    # Create project first
    new_project(ctx, name=project_name)

    # Attempt to create again should raise SystemExit
    with pytest.raises(SystemExit) as exc_info:
        new_project(ctx, name=project_name)

    assert exc_info.value.code == 1


def test_load_regenerates_stl_files_from_config(temp_project_dir: Path) -> None:
    """Test load regenerates all STL files from config."""
    from invoke_collections.gf import load, new_project

    ctx = MockContext()
    project_name = "load-test-project"

    # Create project first
    new_project(ctx, name=project_name)

    # Manually add components to config
    config = {
        "name": project_name,
        "components": [
            {"name": "test-bin", "type": "bin", "length": 1, "width": 1, "height": 1},
            {"name": "test-base", "type": "baseplate", "length": 1, "width": 1},
        ],
    }
    projects.save_project_config(project_name, config)

    # Clear active project to test load sets it
    active_file = temp_project_dir / ".gridfinity-active"
    if active_file.exists():
        active_file.unlink()

    # Load the project
    load(ctx, project=project_name)

    # Verify STL files were generated
    project_dir = temp_project_dir / "projects" / project_name
    assert (project_dir / "test-bin.stl").exists()
    assert (project_dir / "test-base.stl").exists()

    # Verify project is now active
    assert projects.get_active_project() == project_name


def test_list_projects_shows_projects_with_active_indicator(
    temp_project_dir: Path, capsys: pytest.CaptureFixture
) -> None:
    """Test list-projects shows all projects with active indicator."""
    from invoke_collections.gf import list_projects, new_project

    ctx = MockContext()

    # Create multiple projects
    new_project(ctx, name="project-a")
    new_project(ctx, name="project-b")

    # project-b is now active (last created), call list-projects
    list_projects(ctx)

    captured = capsys.readouterr()

    # Both projects should be listed
    assert "project-a" in captured.out
    assert "project-b" in captured.out

    # project-b should have the active indicator
    assert "* project-b" in captured.out or "project-b *" in captured.out


def test_list_projects_shows_no_projects_when_empty(
    temp_project_dir: Path, capsys: pytest.CaptureFixture
) -> None:
    """Test list-projects shows 'No projects found' when empty."""
    from invoke_collections.gf import list_projects

    ctx = MockContext()

    list_projects(ctx)

    captured = capsys.readouterr()
    assert "No projects found" in captured.out
