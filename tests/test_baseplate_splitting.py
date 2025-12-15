"""Tests for interactive baseplate splitting functionality."""

import tempfile
from pathlib import Path

from gridfinity_invoke.generators import (
    calculate_baseplate_splits,
    generate_split_baseplates,
    get_max_units,
)


def test_split_calculation_x_overflow_only() -> None:
    """Test split calculation when only X dimension exceeds max (12x5 -> 3 pieces)."""
    # 12 units wide, 5 units deep, with 5x5 max
    # Should split into 3 pieces: 5x5, 5x5, 2x5
    splits = calculate_baseplate_splits(12, 5)

    assert len(splits) == 3
    assert splits[0] == (5, 5)
    assert splits[1] == (5, 5)
    assert splits[2] == (2, 5)


def test_split_calculation_y_overflow_only() -> None:
    """Test split calculation when only Y dimension exceeds max (5x12 -> 3 pieces)."""
    # 5 units wide, 12 units deep, with 5x5 max
    # Should split into 3 pieces: 5x5, 5x5, 5x2
    splits = calculate_baseplate_splits(5, 12)

    assert len(splits) == 3
    assert splits[0] == (5, 5)
    assert splits[1] == (5, 5)
    assert splits[2] == (5, 2)


def test_split_calculation_both_overflow() -> None:
    """Test split calculation when both dimensions exceed max (10x10 -> 4 pieces)."""
    # 10 units wide, 10 units deep, with 5x5 max
    # Should create 2x2 grid: 4 pieces all 5x5
    splits = calculate_baseplate_splits(10, 10)

    assert len(splits) == 4
    assert splits[0] == (5, 5)
    assert splits[1] == (5, 5)
    assert splits[2] == (5, 5)
    assert splits[3] == (5, 5)


def test_split_calculation_both_overflow_with_remainder() -> None:
    """Test split calculation with remainders in both dimensions (12x7 -> 6 pieces)."""
    # 12 units wide (5+5+2), 7 units deep (5+2), with 5x5 max
    # Should create 3x2 grid: 6 pieces
    splits = calculate_baseplate_splits(12, 7)

    assert len(splits) == 6
    # First row: 5x5, 5x5, 2x5
    assert splits[0] == (5, 5)
    assert splits[1] == (5, 5)
    assert splits[2] == (2, 5)
    # Second row: 5x2, 5x2, 2x2
    assert splits[3] == (5, 2)
    assert splits[4] == (5, 2)
    assert splits[5] == (2, 2)


def test_split_calculation_no_overflow() -> None:
    """Test split calculation when no splitting needed (3x3 -> 1 piece)."""
    # 3 units wide, 3 units deep, with 5x5 max
    # Should return single piece: 3x3
    splits = calculate_baseplate_splits(3, 3)

    assert len(splits) == 1
    assert splits[0] == (3, 3)


def test_generate_split_baseplates_creates_numbered_files() -> None:
    """Test that multiple STL files are generated with correct naming pattern."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Generate 3 split baseplates (simulating 12x5 split)
        splits = [(5, 5), (5, 5), (2, 5)]
        result_paths = generate_split_baseplates(splits, tmpdir_path, "baseplate")

        # Should generate 3 files
        assert len(result_paths) == 3

        # Check naming pattern
        assert result_paths[0].name == "baseplate-1.stl"
        assert result_paths[1].name == "baseplate-2.stl"
        assert result_paths[2].name == "baseplate-3.stl"

        # Verify all files exist and have content
        for path in result_paths:
            assert path.exists()
            assert path.stat().st_size > 0


def test_generate_split_baseplates_with_project_name() -> None:
    """Test split baseplate generation with project component naming."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Generate split baseplates with project-style name
        splits = [(5, 5), (5, 5)]
        result_paths = generate_split_baseplates(
            splits, tmpdir_path, "drawer-fit-530x247mm-baseplate"
        )

        # Should generate 2 files with project naming
        assert len(result_paths) == 2
        assert result_paths[0].name == "drawer-fit-530x247mm-baseplate-1.stl"
        assert result_paths[1].name == "drawer-fit-530x247mm-baseplate-2.stl"


def test_get_max_units_returns_correct_values_for_default() -> None:
    """Test that get_max_units returns correct values for default 225mm bed."""
    # Default config should return 225mm bed (5x5 units)
    max_x, max_y = get_max_units()

    assert max_x == 5  # 225 // 42 = 5
    assert max_y == 5  # 225 // 42 = 5


def test_split_calculation_respects_max_units() -> None:
    """Test that split calculation respects max units from configuration."""
    # Get current max units
    max_x, max_y = get_max_units()

    # Test that splits respect these constants
    # 6 units should split into [max_x, 1] if max_x=5
    splits = calculate_baseplate_splits(6, 1)
    assert len(splits) == 2
    assert splits[0][0] == max_x  # First piece width
    assert splits[1][0] == 1  # Second piece width (remainder)
