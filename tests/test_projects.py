"""Tests for project management module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gridfinity_invoke import projects


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for project tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        active_file = tmpdir_path / ".gridfinity-active"
        with patch.object(projects, "PROJECTS_DIR", tmpdir_path / "projects"):
            with patch.object(projects, "ACTIVE_FILE", active_file):
                yield tmpdir_path


def test_get_active_project_returns_none_when_file_missing(
    temp_project_dir: Path,
) -> None:
    """Test get_active_project returns None when .gridfinity-active missing."""
    result = projects.get_active_project()
    assert result is None


def test_set_active_project_creates_file_with_name(temp_project_dir: Path) -> None:
    """Test that set_active_project creates .gridfinity-active with project name."""
    projects.set_active_project("my-test-project")

    active_file = temp_project_dir / ".gridfinity-active"
    assert active_file.exists()
    assert active_file.read_text().strip() == "my-test-project"

    # Verify get_active_project reads it back
    assert projects.get_active_project() == "my-test-project"


def test_load_project_config_reads_and_parses_json(temp_project_dir: Path) -> None:
    """Test that load_project_config reads and parses config.json correctly."""
    project_name = "test-project"
    project_dir = temp_project_dir / "projects" / project_name
    project_dir.mkdir(parents=True)

    config = {
        "name": project_name,
        "components": [
            {"name": "main-bin", "type": "bin", "length": 2, "width": 2, "height": 3}
        ],
    }
    config_file = project_dir / "config.json"
    config_file.write_text(json.dumps(config))

    result = projects.load_project_config(project_name)
    assert result == config
    assert result["name"] == project_name
    assert len(result["components"]) == 1


def test_save_project_config_writes_valid_json(temp_project_dir: Path) -> None:
    """Test that save_project_config writes valid JSON to config.json."""
    project_name = "new-project"
    config = {
        "name": project_name,
        "components": [{"name": "base", "type": "baseplate", "length": 4, "width": 4}],
    }

    projects.save_project_config(project_name, config)

    config_file = temp_project_dir / "projects" / project_name / "config.json"
    assert config_file.exists()

    # Verify it's valid JSON that can be parsed back
    loaded = json.loads(config_file.read_text())
    assert loaded == config


def test_add_component_to_config_adds_new_and_updates_duplicates(
    temp_project_dir: Path,
) -> None:
    """Test add_component_to_config adds new components and updates by name."""
    project_name = "component-test"
    initial_config = {"name": project_name, "components": []}
    projects.save_project_config(project_name, initial_config)

    # Add first component
    component1 = {"name": "bin-1", "type": "bin", "length": 2, "width": 2, "height": 3}
    projects.add_component_to_config(project_name, component1)

    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 1
    assert config["components"][0] == component1

    # Add second component
    component2 = {"name": "base-1", "type": "baseplate", "length": 4, "width": 4}
    projects.add_component_to_config(project_name, component2)

    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 2

    # Update existing component (same name, different dimensions)
    component1_updated = {
        "name": "bin-1",
        "type": "bin",
        "length": 3,
        "width": 3,
        "height": 4,
    }
    projects.add_component_to_config(project_name, component1_updated)

    config = projects.load_project_config(project_name)
    assert len(config["components"]) == 2  # Should still be 2, not 3

    # Verify the component was updated, not added
    bin_component = next(c for c in config["components"] if c["name"] == "bin-1")
    assert bin_component["length"] == 3
    assert bin_component["height"] == 4
