"""Tests for drawer fit generator function."""

import tempfile
from pathlib import Path

import pytest

from gridfinity_invoke.generators import (
    GRIDFINITY_UNIT_MM,
    MIN_SPACER_GAP_MM,
    generate_drawer_fit,
    get_max_units,
)


def test_mm_to_gridfinity_unit_conversion() -> None:
    """Test mm to gridfinity unit conversion: 200mm -> 4 units, 168mm actual."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseplate_path = tmpdir_path / "baseplate.stl"
        spacer_path = tmpdir_path / "spacers.stl"

        result = generate_drawer_fit(200.0, 200.0, baseplate_path, spacer_path)

        # 200mm // 42mm = 4 units
        assert result.units_width == 4
        assert result.units_depth == 4
        # 4 units * 42mm = 168mm actual
        assert result.actual_width_mm == 168.0
        assert result.actual_depth_mm == 168.0


def test_floor_rounding_behavior() -> None:
    """Test floor rounding: 125mm -> 2 units (not 3), ensuring fit."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseplate_path = tmpdir_path / "baseplate.stl"
        spacer_path = tmpdir_path / "spacers.stl"

        result = generate_drawer_fit(125.0, 125.0, baseplate_path, spacer_path)

        # 125mm // 42mm = 2 units (floor), not 3 (round)
        assert result.units_width == 2
        assert result.units_depth == 2
        # Actual size is 84mm, which fits in 125mm drawer
        assert result.actual_width_mm == 84.0
        assert result.actual_depth_mm == 84.0


def test_minimum_dimension_validation() -> None:
    """Test that dimensions < 42mm raise ValueError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseplate_path = tmpdir_path / "baseplate.stl"
        spacer_path = tmpdir_path / "spacers.stl"

        # Width too small
        with pytest.raises(ValueError, match="42mm"):
            generate_drawer_fit(30.0, 100.0, baseplate_path, spacer_path)

        # Depth too small
        with pytest.raises(ValueError, match="42mm"):
            generate_drawer_fit(100.0, 30.0, baseplate_path, spacer_path)


def test_gap_calculations() -> None:
    """Test gap calculations: 200mm drawer, 4 units = 168mm, gap = 32mm total."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseplate_path = tmpdir_path / "baseplate.stl"
        spacer_path = tmpdir_path / "spacers.stl"

        result = generate_drawer_fit(200.0, 200.0, baseplate_path, spacer_path)

        # Gap = input - actual = 200 - 168 = 32mm
        assert result.gap_x_mm == 32.0
        assert result.gap_y_mm == 32.0


def test_baseplate_stl_file_created() -> None:
    """Test that baseplate STL file is created at expected path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        baseplate_path = tmpdir_path / "output" / "baseplate.stl"
        spacer_path = tmpdir_path / "output" / "spacers.stl"

        result = generate_drawer_fit(200.0, 200.0, baseplate_path, spacer_path)

        # Verify baseplate file exists
        assert result.baseplate_path.exists()
        assert result.baseplate_path == baseplate_path
        # Verify file has content (non-empty STL)
        assert result.baseplate_path.stat().st_size > 0


def test_dynamic_max_units_function() -> None:
    """Test get_max_units function returns configuration-based values."""
    # Get max units from current configuration
    max_x, max_y = get_max_units()

    # Both should be positive integers
    assert isinstance(max_x, int)
    assert isinstance(max_y, int)
    assert max_x > 0
    assert max_y > 0

    # Should match calculation: bed_size // 42
    # Default config is 225mm, so 225 // 42 = 5
    assert max_x >= 1  # At least 1 unit should fit
    assert max_y >= 1


def test_gridfinity_constants_unchanged() -> None:
    """Test that gridfinity standard constants remain fixed."""
    # These should never change - they're part of the Gridfinity standard
    assert GRIDFINITY_UNIT_MM == 42
    assert MIN_SPACER_GAP_MM == 4
