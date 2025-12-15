"""Tests for generator module using config values."""

from pathlib import Path

import pytest

import gridfinity_invoke.config as config
import gridfinity_invoke.generators as generators


@pytest.fixture(autouse=True)
def temp_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set up a temporary config directory for tests."""
    config_file = tmp_path / ".gf-config"
    monkeypatch.setattr(config, "CONFIG_FILE", config_file)
    return tmp_path


def test_get_max_units_returns_defaults_when_no_config(
    temp_config_dir: Path,
) -> None:
    """Test get_max_units returns defaults when config doesn't exist."""
    # No config file exists, should return defaults (225mm = 5 units)
    max_units_x, max_units_y = generators.get_max_units()

    assert max_units_x == 5  # 225 // 42 = 5
    assert max_units_y == 5


def test_get_max_units_uses_config_values(temp_config_dir: Path) -> None:
    """Test get_max_units uses values from config file."""
    # Save a config with custom bed size: 300mm x 200mm
    custom_config = {
        "print_bed_width_mm": 300,
        "print_bed_depth_mm": 200,
    }
    config.save_printer_config(custom_config)

    # Should calculate max units from config
    max_units_x, max_units_y = generators.get_max_units()

    # 300 // 42 = 7, 200 // 42 = 4
    assert max_units_x == 7
    assert max_units_y == 4


def test_generate_drawer_fit_uses_config_for_constraints(
    temp_config_dir: Path, tmp_path: Path
) -> None:
    """Test generate_drawer_fit respects config values for constraints."""
    # Save custom config
    custom_config = {
        "print_bed_width_mm": 300,
        "print_bed_depth_mm": 200,
    }
    config.save_printer_config(custom_config)

    # Generate a drawer fit solution
    baseplate_path = tmp_path / "baseplate.stl"
    spacer_path = tmp_path / "spacers.stl"

    result = generators.generate_drawer_fit(200, 150, baseplate_path, spacer_path)

    # Should calculate units correctly
    assert result.units_width == 4  # 200 // 42 = 4
    assert result.units_depth == 3  # 150 // 42 = 3


def test_calculate_baseplate_splits_uses_config_values(
    temp_config_dir: Path,
) -> None:
    """Test baseplate splits uses config instead of hardcoded values."""
    # Save custom config: 168mm x 126mm bed (4x3 units)
    custom_config = {
        "print_bed_width_mm": 168,  # 168 // 42 = 4 units
        "print_bed_depth_mm": 126,  # 126 // 42 = 3 units
    }
    config.save_printer_config(custom_config)

    # Try to split a 10x10 baseplate
    splits = generators.calculate_baseplate_splits(10, 10)

    # With 4x3 max, should split into:
    # X: 4 + 4 + 2 = 3 pieces
    # Y: 3 + 3 + 3 + 1 = 4 pieces
    # Total: 3 * 4 = 12 pieces
    assert len(splits) == 12

    # Verify first few pieces
    assert splits[0] == (4, 3)  # First piece should be max size
    assert splits[1] == (4, 3)  # Second piece in X row
    assert splits[2] == (2, 3)  # Last piece in X row (remainder)
