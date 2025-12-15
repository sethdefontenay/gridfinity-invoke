"""Tests for printer configuration module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gridfinity_invoke import config


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        config_file = tmpdir_path / ".gf-config"
        with patch.object(config, "CONFIG_FILE", config_file):
            yield tmpdir_path


def test_load_printer_config_returns_defaults_when_file_missing(
    temp_config_dir: Path,
) -> None:
    """Test load_printer_config returns defaults when .gf-config missing."""
    result = config.load_printer_config()

    assert result["print_bed_width_mm"] == 225
    assert result["print_bed_depth_mm"] == 225


def test_load_printer_config_reads_existing_json_correctly(
    temp_config_dir: Path,
) -> None:
    """Test load_printer_config reads existing .gf-config JSON correctly."""
    config_file = temp_config_dir / ".gf-config"
    config_data = {
        "print_bed_width_mm": 300,
        "print_bed_depth_mm": 250,
    }
    config_file.write_text(json.dumps(config_data))

    result = config.load_printer_config()

    assert result["print_bed_width_mm"] == 300
    assert result["print_bed_depth_mm"] == 250


def test_save_printer_config_creates_and_updates_file_with_indent(
    temp_config_dir: Path,
) -> None:
    """Test save_printer_config creates/updates .gf-config with JSON indent=2."""
    config_data = {
        "print_bed_width_mm": 350,
        "print_bed_depth_mm": 300,
    }

    config.save_printer_config(config_data)

    config_file = temp_config_dir / ".gf-config"
    assert config_file.exists()

    # Verify JSON format with indent=2
    saved_text = config_file.read_text()
    assert "  " in saved_text  # Check for indentation

    # Verify it can be parsed back
    loaded = json.loads(saved_text)
    assert loaded == config_data


def test_get_print_bed_dimensions_returns_tuple(temp_config_dir: Path) -> None:
    """Test get_print_bed_dimensions returns tuple of (width, depth)."""
    config_data = {
        "print_bed_width_mm": 400,
        "print_bed_depth_mm": 350,
    }
    config.save_printer_config(config_data)

    width, depth = config.get_print_bed_dimensions()

    assert width == 400
    assert depth == 350
    assert isinstance(width, int)
    assert isinstance(depth, int)


def test_config_values_are_parsed_as_integers(temp_config_dir: Path) -> None:
    """Test config values are properly parsed as integers."""
    config_file = temp_config_dir / ".gf-config"
    config_data = {
        "print_bed_width_mm": 280,
        "print_bed_depth_mm": 260,
    }
    config_file.write_text(json.dumps(config_data))

    result = config.load_printer_config()

    assert isinstance(result["print_bed_width_mm"], int)
    assert isinstance(result["print_bed_depth_mm"], int)
    assert result["print_bed_width_mm"] == 280
    assert result["print_bed_depth_mm"] == 260


# Task Group 4: Auto-prompt Integration Tests


def test_ensure_printer_config_prompts_when_config_missing(
    temp_config_dir: Path,
) -> None:
    """Test ensure_printer_config prompts when .gf-config missing."""
    # Mock the prompt function to return test values
    mock_prompt = MagicMock(side_effect=["300", "250"])

    with patch("invoke_collections.helpers.prompt_with_default", mock_prompt):
        config.ensure_printer_config()

    # Verify config was saved
    config_file = temp_config_dir / ".gf-config"
    assert config_file.exists()

    # Verify saved values
    saved_config = json.loads(config_file.read_text())
    assert saved_config["print_bed_width_mm"] == 300
    assert saved_config["print_bed_depth_mm"] == 250


def test_ensure_printer_config_saves_prompted_values(
    temp_config_dir: Path,
) -> None:
    """Test prompted values are saved to .gf-config."""
    # Mock the prompt function
    mock_prompt = MagicMock(side_effect=["350", "275"])

    with patch("invoke_collections.helpers.prompt_with_default", mock_prompt):
        config.ensure_printer_config()

    # Verify the file was created and contains correct values
    saved_config = config.load_printer_config()
    assert saved_config["print_bed_width_mm"] == 350
    assert saved_config["print_bed_depth_mm"] == 275


def test_ensure_printer_config_uses_existing_values_silently(
    temp_config_dir: Path, capsys
) -> None:
    """Test existing config values are used silently with log message."""
    # Create existing config
    config_file = temp_config_dir / ".gf-config"
    config_data = {
        "print_bed_width_mm": 400,
        "print_bed_depth_mm": 350,
    }
    config_file.write_text(json.dumps(config_data))

    # Call ensure_printer_config - should not prompt
    mock_prompt = MagicMock()
    with patch("invoke_collections.helpers.prompt_with_default", mock_prompt):
        config.ensure_printer_config()

    # Verify prompt was NOT called
    mock_prompt.assert_not_called()

    # Verify log message was printed
    captured = capsys.readouterr()
    assert (
        "Using printer config" in captured.out
        or "printer config" in captured.out.lower()
    )


# Task Group 6: Strategic End-to-End Tests


def test_config_workflow_complete_cycle(temp_config_dir: Path) -> None:
    """Test complete workflow: save, load, update config multiple times."""
    # First save
    config_v1 = {"print_bed_width_mm": 220, "print_bed_depth_mm": 220}
    config.save_printer_config(config_v1)

    # Load and verify
    loaded_v1 = config.load_printer_config()
    assert loaded_v1 == config_v1

    # Update config
    config_v2 = {"print_bed_width_mm": 300, "print_bed_depth_mm": 250}
    config.save_printer_config(config_v2)

    # Load and verify update
    loaded_v2 = config.load_printer_config()
    assert loaded_v2 == config_v2
    assert loaded_v2 != config_v1

    # Verify file format is still correct
    config_file = temp_config_dir / ".gf-config"
    file_content = config_file.read_text()
    parsed = json.loads(file_content)
    assert parsed == config_v2


def test_config_file_format_matches_specification(temp_config_dir: Path) -> None:
    """Test that saved config file exactly matches JSON format specification."""
    config_data = {
        "print_bed_width_mm": 225,
        "print_bed_depth_mm": 225,
    }
    config.save_printer_config(config_data)

    # Read raw file content
    config_file = temp_config_dir / ".gf-config"
    file_content = config_file.read_text()

    # Verify it's valid JSON with indent=2
    parsed = json.loads(file_content)
    assert parsed == config_data

    # Verify indent=2 formatting (should have 2-space indentation)
    assert '{\n  "print_bed_width_mm":' in file_content
    assert '  "print_bed_depth_mm":' in file_content


def test_config_handles_missing_file_gracefully_on_multiple_operations(
    temp_config_dir: Path,
) -> None:
    """Test that config operations handle missing file consistently."""
    # First load should return defaults
    result1 = config.load_printer_config()
    assert result1["print_bed_width_mm"] == 225

    # Multiple loads without file should all return defaults
    result2 = config.load_printer_config()
    result3 = config.load_printer_config()
    assert result1 == result2 == result3

    # File still shouldn't exist
    config_file = temp_config_dir / ".gf-config"
    assert not config_file.exists()


def test_get_print_bed_dimensions_works_with_missing_config(
    temp_config_dir: Path,
) -> None:
    """Test get_print_bed_dimensions returns defaults when config missing."""
    # No config file exists
    config_file = temp_config_dir / ".gf-config"
    assert not config_file.exists()

    # Should return default dimensions
    width, depth = config.get_print_bed_dimensions()
    assert width == 225
    assert depth == 225


def test_ensure_printer_config_creates_valid_json_format(
    temp_config_dir: Path,
) -> None:
    """Test ensure_printer_config creates properly formatted JSON file."""
    # Mock prompts
    mock_prompt = MagicMock(side_effect=["280", "260"])

    with patch("invoke_collections.helpers.prompt_with_default", mock_prompt):
        config.ensure_printer_config()

    # Verify file exists and is valid JSON
    config_file = temp_config_dir / ".gf-config"
    assert config_file.exists()

    # Parse and verify format
    content = config_file.read_text()
    parsed = json.loads(content)

    assert parsed["print_bed_width_mm"] == 280
    assert parsed["print_bed_depth_mm"] == 260

    # Verify indent=2 formatting
    assert '{\n  "print_bed_width_mm":' in content
