"""Gridfinity component generation using cqgridfinity."""

from pathlib import Path

from cqgridfinity import GridfinityBaseplate, GridfinityBox


def generate_bin(
    length: int,
    width: int,
    height: int,
    output_path: str | Path,
) -> Path:
    """Generate a Gridfinity bin and export to STL.

    Args:
        length: Length in gridfinity units (1 unit = 42mm)
        width: Width in gridfinity units
        height: Height in gridfinity units (1 unit = 7mm)
        output_path: Path to write the STL file

    Returns:
        Path to the generated STL file

    Raises:
        ValueError: If dimensions are not positive integers
    """
    if length < 1 or width < 1 or height < 1:
        raise ValueError("All dimensions must be positive integers >= 1")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    box = GridfinityBox(length, width, height)
    result = box.render()
    result.val().exportStl(str(output_path))

    return output_path


def generate_baseplate(
    length: int,
    width: int,
    output_path: str | Path,
) -> Path:
    """Generate a Gridfinity baseplate and export to STL.

    Args:
        length: Length in gridfinity units (1 unit = 42mm)
        width: Width in gridfinity units
        output_path: Path to write the STL file

    Returns:
        Path to the generated STL file

    Raises:
        ValueError: If dimensions are not positive integers
    """
    if length < 1 or width < 1:
        raise ValueError("All dimensions must be positive integers >= 1")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    baseplate = GridfinityBaseplate(length, width)
    result = baseplate.render()
    result.val().exportStl(str(output_path))

    return output_path
