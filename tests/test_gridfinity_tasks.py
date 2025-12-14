"""Tests for gridfinity generation tasks (bin, baseplate)."""

import tempfile
from pathlib import Path

import pytest

from gridfinity_invoke.generators import generate_baseplate, generate_bin


def test_bin_generates_valid_stl_output() -> None:
    """Test that bin generator creates a valid STL file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_bin.stl"
        result = generate_bin(2, 2, 3, output_path)

        assert result.exists()
        assert result.stat().st_size > 0
        # STL files start with "solid" (ASCII) or have binary header
        content = result.read_bytes()
        assert len(content) > 1000  # Should be a reasonably sized mesh


def test_baseplate_generates_valid_stl_output() -> None:
    """Test that baseplate generator creates a valid STL file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_baseplate.stl"
        result = generate_baseplate(4, 4, output_path)

        assert result.exists()
        assert result.stat().st_size > 0
        content = result.read_bytes()
        assert len(content) > 1000


def test_output_file_created_at_specified_location() -> None:
    """Test that output file is created at the exact path specified."""
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_path = Path(tmpdir) / "subdir" / "custom_name.stl"
        result = generate_bin(1, 1, 2, custom_path)

        assert result == custom_path
        assert custom_path.exists()


def test_invalid_dimensions_raise_error() -> None:
    """Test that invalid dimensions raise appropriate errors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.stl"

        with pytest.raises(ValueError, match="positive integers"):
            generate_bin(0, 2, 3, output_path)

        with pytest.raises(ValueError, match="positive integers"):
            generate_bin(2, -1, 3, output_path)

        with pytest.raises(ValueError, match="positive integers"):
            generate_baseplate(0, 4, output_path)
