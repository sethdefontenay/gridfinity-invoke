"""Gridfinity component generation using cqgridfinity."""

from pathlib import Path
from typing import NamedTuple

from cqgridfinity import GridfinityBaseplate, GridfinityBox, GridfinityDrawerSpacer

from gridfinity_invoke.config import get_print_bed_dimensions

# Gridfinity standard constants
GRIDFINITY_UNIT_MM = 42  # 1 gridfinity unit = 42mm
MIN_SPACER_GAP_MM = 4  # cqgridfinity threshold for spacer generation


def get_max_units() -> tuple[int, int]:
    """Get maximum gridfinity units that fit on the print bed.

    Returns:
        Tuple of (max_units_x, max_units_y) based on current printer configuration.
    """
    bed_width, bed_depth = get_print_bed_dimensions()
    max_units_x = bed_width // GRIDFINITY_UNIT_MM
    max_units_y = bed_depth // GRIDFINITY_UNIT_MM
    return (max_units_x, max_units_y)


class DrawerFitResult(NamedTuple):
    """Result from generate_drawer_fit containing paths and calculation metadata."""

    baseplate_path: Path
    spacer_path: Path | None  # None if no spacers needed
    units_width: int
    units_depth: int
    actual_width_mm: float
    actual_depth_mm: float
    gap_x_mm: float  # Total gap in X direction
    gap_y_mm: float  # Total gap in Y direction


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
    result.val().exportStl(str(output_path))  # pyrefly: ignore[missing-attribute]

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
    result.val().exportStl(str(output_path))  # pyrefly: ignore[missing-attribute]

    return output_path


def calculate_baseplate_splits(units_x: int, units_y: int) -> list[tuple[int, int]]:
    """Calculate how to split an oversized baseplate into printable pieces.

    For dimensions that exceed the maximum printable units, splits the baseplate
    into a grid of smaller pieces. Each piece is at most the maximum printable
    units in each dimension, with the final piece in each direction getting the
    remainder.

    Args:
        units_x: Total width in gridfinity units
        units_y: Total depth in gridfinity units

    Returns:
        List of (width, depth) tuples for each piece. If no splitting needed,
        returns a single-item list with the original dimensions.

    Examples:
        >>> calculate_baseplate_splits(12, 5)  # Max 5x5
        [(5, 5), (5, 5), (2, 5)]  # 3 pieces in X direction

        >>> calculate_baseplate_splits(12, 7)  # Max 5x5
        [(5, 5), (5, 5), (2, 5), (5, 2), (5, 2), (2, 2)]  # 3x2 grid = 6 pieces
    """
    # Get max units from current printer configuration
    max_units_x, max_units_y = get_max_units()

    # Calculate how many pieces needed in each direction
    num_pieces_x = (units_x + max_units_x - 1) // max_units_x
    num_pieces_y = (units_y + max_units_y - 1) // max_units_y

    # Build list of piece sizes for each direction
    pieces_x = []
    remaining_x = units_x
    for _ in range(num_pieces_x):
        piece_width = min(remaining_x, max_units_x)
        pieces_x.append(piece_width)
        remaining_x -= piece_width

    pieces_y = []
    remaining_y = units_y
    for _ in range(num_pieces_y):
        piece_depth = min(remaining_y, max_units_y)
        pieces_y.append(piece_depth)
        remaining_y -= piece_depth

    # Create grid of pieces (X pieces * Y pieces)
    splits = []
    for y_size in pieces_y:
        for x_size in pieces_x:
            splits.append((x_size, y_size))

    return splits


def generate_split_baseplates(
    splits: list[tuple[int, int]], output_dir: Path, base_name: str
) -> list[Path]:
    """Generate multiple baseplate STL files from split calculations.

    Creates numbered baseplate files for each piece in the split calculation.
    Uses the naming pattern: {base_name}-1.stl, {base_name}-2.stl, etc.

    Args:
        splits: List of (width, depth) tuples for each piece from
            calculate_baseplate_splits
        output_dir: Directory to write the STL files
        base_name: Base name for the files (e.g., "baseplate" or
            "drawer-fit-530x247mm-baseplate")

    Returns:
        List of paths to the generated STL files

    Examples:
        >>> splits = [(5, 5), (5, 5), (2, 5)]
        >>> paths = generate_split_baseplates(splits, Path("output"), "baseplate")
        # Generates: baseplate-1.stl, baseplate-2.stl, baseplate-3.stl
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result_paths = []

    for i, (width, depth) in enumerate(splits, start=1):
        # Generate numbered filename
        output_path = output_dir / f"{base_name}-{i}.stl"

        # Generate baseplate with these dimensions
        baseplate = GridfinityBaseplate(width, depth)
        result = baseplate.render()
        result.val().exportStl(str(output_path))  # pyrefly: ignore[missing-attribute]

        result_paths.append(output_path)

    return result_paths


def generate_drawer_fit(
    width_mm: float,
    depth_mm: float,
    baseplate_path: Path,
    spacer_path: Path,
) -> DrawerFitResult:
    """Generate a complete drawer-fit solution from drawer dimensions.

    Calculates the optimal gridfinity baseplate size to fit the drawer,
    generates the baseplate STL, and optionally generates spacers if
    the gap is large enough (>= 4mm).

    Args:
        width_mm: Drawer width (X dimension) in millimeters
        depth_mm: Drawer depth (Y dimension) in millimeters
        baseplate_path: Path to write the baseplate STL file
        spacer_path: Path to write the spacer STL file (if needed)

    Returns:
        DrawerFitResult with paths and calculation metadata

    Raises:
        ValueError: If either dimension is less than 42mm (minimum for 1x1 baseplate)
    """
    # Validate minimum dimensions
    if width_mm < GRIDFINITY_UNIT_MM:
        raise ValueError(
            f"Width must be at least {GRIDFINITY_UNIT_MM}mm to fit a 1-unit baseplate"
        )
    if depth_mm < GRIDFINITY_UNIT_MM:
        raise ValueError(
            f"Depth must be at least {GRIDFINITY_UNIT_MM}mm to fit a 1-unit baseplate"
        )

    # Convert mm to gridfinity units (floor division for conservative fit)
    units_width = int(width_mm // GRIDFINITY_UNIT_MM)
    units_depth = int(depth_mm // GRIDFINITY_UNIT_MM)

    # Calculate actual dimensions
    actual_width_mm = float(units_width * GRIDFINITY_UNIT_MM)
    actual_depth_mm = float(units_depth * GRIDFINITY_UNIT_MM)

    # Calculate gaps
    gap_x_mm = width_mm - actual_width_mm
    gap_y_mm = depth_mm - actual_depth_mm

    # Generate baseplate
    baseplate_path = Path(baseplate_path)
    baseplate_path.parent.mkdir(parents=True, exist_ok=True)

    baseplate = GridfinityBaseplate(units_width, units_depth)
    result = baseplate.render()
    result.val().exportStl(str(baseplate_path))  # pyrefly: ignore[missing-attribute]

    # Generate spacers only if gap is large enough
    # cqgridfinity uses min_margin=4 as threshold (gap per side must exceed 4mm)
    # Total gap / 2 gives per-side gap; both X and Y must have sufficient margin
    spacer_result_path: Path | None = None
    per_side_gap_x = gap_x_mm / 2
    per_side_gap_y = gap_y_mm / 2

    if per_side_gap_x > MIN_SPACER_GAP_MM or per_side_gap_y > MIN_SPACER_GAP_MM:
        spacer_path = Path(spacer_path)
        spacer_path.parent.mkdir(parents=True, exist_ok=True)

        spacer = GridfinityDrawerSpacer(dr_width=width_mm, dr_depth=depth_mm)
        spacer_obj = spacer.render_half_set()

        if spacer_obj is not None:
            # pyrefly: ignore[missing-attribute]
            spacer_obj.val().exportStl(str(spacer_path))
            spacer_result_path = spacer_path

    return DrawerFitResult(
        baseplate_path=baseplate_path,
        spacer_path=spacer_result_path,
        units_width=units_width,
        units_depth=units_depth,
        actual_width_mm=actual_width_mm,
        actual_depth_mm=actual_depth_mm,
        gap_x_mm=gap_x_mm,
        gap_y_mm=gap_y_mm,
    )
