"""Tests for project-aware bin and baseplate generation tasks."""

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


def test_bin_with_active_project_suggests_default_name(
    temp_project_dir: Path,
) -> None:
    """Test bin with active project suggests default name like bin-2x2x3."""
    from tasks import new_project, prompt_with_default

    ctx = MockContext()
    project_name = "test-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Check that default name format is correct
    default_name = "bin-2x2x3"

    # Verify active project is set
    assert projects.get_active_project() == project_name

    # Test the prompt_with_default function returns default when empty input
    with patch("builtins.input", return_value=""):
        result = prompt_with_default("Name", default_name)
        assert result == default_name


def test_bin_saves_to_project_directory_and_updates_config(
    temp_project_dir: Path,
) -> None:
    """Test bin saves to project directory and updates config."""
    from tasks import bin, new_project

    ctx = MockContext()
    project_name = "bin-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Mock user input to accept default name
    with patch("tasks.prompt_with_default", return_value="bin-2x2x3"):
        bin(ctx, length=2, width=2, height=3)

    # Verify STL was saved to project directory
    project_dir = temp_project_dir / "projects" / project_name
    stl_file = project_dir / "bin-2x2x3.stl"
    assert stl_file.exists()

    # Verify config was updated
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1
    component = config["components"][0]
    assert component["name"] == "bin-2x2x3"
    assert component["type"] == "bin"
    assert component["length"] == 2
    assert component["width"] == 2
    assert component["height"] == 3


def test_bin_without_active_project_uses_default_behavior(
    temp_project_dir: Path,
) -> None:
    """Test bin without active project uses existing output/ behavior."""
    from tasks import bin

    ctx = MockContext()

    # Ensure no active project (temp_project_dir has no .gridfinity-active)
    assert projects.get_active_project() is None

    # Create output directory in temp location
    output_dir = temp_project_dir / "output"
    output_path = output_dir / "bin.stl"

    # Run bin with explicit output path (default behavior)
    bin(ctx, length=1, width=1, height=1, output=str(output_path))

    # Verify STL was saved to output directory
    assert output_path.exists()


def test_baseplate_with_active_project_suggests_default_name(
    temp_project_dir: Path,
) -> None:
    """Test baseplate with active project suggests default name like baseplate-4x4."""
    from tasks import new_project, prompt_with_default

    ctx = MockContext()
    project_name = "baseplate-test-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Check that default name format is correct
    default_name = "baseplate-4x4"

    # Verify active project is set
    assert projects.get_active_project() == project_name

    # Test the prompt_with_default function returns default when empty input
    with patch("builtins.input", return_value=""):
        result = prompt_with_default("Name", default_name)
        assert result == default_name


def test_baseplate_saves_to_project_directory_and_updates_config(
    temp_project_dir: Path,
) -> None:
    """Test baseplate saves to project directory and updates config."""
    from tasks import baseplate, new_project

    ctx = MockContext()
    project_name = "baseplate-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Mock user input to accept default name
    with patch("tasks.prompt_with_default", return_value="baseplate-4x4"):
        baseplate(ctx, length=4, width=4)

    # Verify STL was saved to project directory
    project_dir = temp_project_dir / "projects" / project_name
    stl_file = project_dir / "baseplate-4x4.stl"
    assert stl_file.exists()

    # Verify config was updated
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1
    component = config["components"][0]
    assert component["name"] == "baseplate-4x4"
    assert component["type"] == "baseplate"
    assert component["length"] == 4
    assert component["width"] == 4


def test_component_name_deduplication_in_config(temp_project_dir: Path) -> None:
    """Test component name deduplication in config when same name used twice."""
    from tasks import bin, new_project

    ctx = MockContext()
    project_name = "dedup-project"

    # Create and set active project
    new_project(ctx, name=project_name)

    # Add first bin with custom name
    with patch("tasks.prompt_with_default", return_value="my-bin"):
        bin(ctx, length=1, width=1, height=1)

    # Add second bin with same name but different dimensions
    with patch("tasks.prompt_with_default", return_value="my-bin"):
        bin(ctx, length=2, width=2, height=2)

    # Verify config has only one component (deduplicated)
    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1

    # Verify the component was updated with new dimensions
    component = config["components"][0]
    assert component["name"] == "my-bin"
    assert component["length"] == 2
    assert component["width"] == 2
    assert component["height"] == 2
