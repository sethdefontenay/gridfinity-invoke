"""Tests for drawer-fit project integration.

These tests verify that the drawer-fit task properly integrates with
the project save/load system.
"""

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


def test_drawer_fit_with_active_project_prompts_for_name(
    temp_project_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test drawer-fit with active project prompts for component name."""
    from tasks import drawer_fit, new_project

    ctx = MockContext()
    project_name = "drawer-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Run drawer-fit with active project and mock the prompt
    mock_return = "kitchen-drawer"
    with patch("tasks.prompt_with_default", return_value=mock_return) as mock_prompt:
        drawer_fit(ctx, width=200.0, depth=200.0)

    # Verify prompt was called with correct default format
    mock_prompt.assert_called_once()
    call_args = mock_prompt.call_args
    assert call_args[0][0] == "Name"  # First positional arg is the prompt text
    assert "drawer-fit-200" in call_args[0][1]  # Default name contains dimensions


def test_drawer_fit_saves_stl_files_to_project_directory(
    temp_project_dir: Path,
) -> None:
    """Test drawer-fit saves both STL files to project directory."""
    from tasks import drawer_fit, new_project

    ctx = MockContext()
    project_name = "stl-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Run drawer-fit with active project
    with patch("tasks.prompt_with_default", return_value="my-drawer"):
        drawer_fit(ctx, width=200.0, depth=200.0)

    # Verify STL files were created in project directory
    project_dir = temp_project_dir / "projects" / project_name
    assert (project_dir / "my-drawer-baseplate.stl").exists()
    # Spacers created when gap is large enough (200mm -> 4 units = 168mm, gap = 32mm)
    assert (project_dir / "my-drawer-spacers.stl").exists()


def test_drawer_fit_adds_component_to_config_with_type(
    temp_project_dir: Path,
) -> None:
    """Test drawer-fit adds component to config with type 'drawer-fit'."""
    from tasks import drawer_fit, new_project

    ctx = MockContext()
    project_name = "config-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Run drawer-fit with active project
    with patch("tasks.prompt_with_default", return_value="office-drawer"):
        drawer_fit(ctx, width=500.0, depth=400.0)

    # Verify component was added to config
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1

    component = config["components"][0]
    assert component["name"] == "office-drawer"
    assert component["type"] == "drawer-fit"
    assert component["width_mm"] == 500.0
    assert component["depth_mm"] == 400.0
    assert component["units_width"] == 11  # 500 / 42 = 11
    assert component["units_depth"] == 9  # 400 / 42 = 9


def test_drawer_fit_without_active_project_uses_default_output(
    temp_project_dir: Path,
) -> None:
    """Test drawer-fit without active project uses default output directory."""
    from tasks import drawer_fit

    ctx = MockContext()

    # Create a temp output directory (no active project)
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = str(Path(tmpdir) / "drawer-fit")

        # Run drawer-fit without active project
        drawer_fit(ctx, width=200.0, depth=200.0, output=output_path)

        # Verify files were created in specified output location
        assert (Path(tmpdir) / "drawer-fit-baseplate.stl").exists()


def test_drawer_fit_project_integration_success_message(
    temp_project_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test drawer-fit displays success message when added to project."""
    from tasks import drawer_fit, new_project

    ctx = MockContext()
    project_name = "message-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Run drawer-fit with active project
    with patch("tasks.prompt_with_default", return_value="test-drawer"):
        drawer_fit(ctx, width=200.0, depth=200.0)

    captured = capsys.readouterr()

    # Verify success message contains project name
    assert "Added to project" in captured.out
    assert project_name in captured.out
