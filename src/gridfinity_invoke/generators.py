"""Gridfinity component generation using cqgridfinity."""

from pathlib import Path
from typing import NamedTuple

from cqgridfinity import GridfinityBaseplate, GridfinityBox, GridfinityDrawerSpacer

# Gridfinity standard constants
GRIDFINITY_UNIT_MM = 42  # 1 gridfinity unit = 42mm
MIN_SPACER_GAP_MM = 4  # cqgridfinity threshold for spacer generation

# Print bed configuration - edit these values for your printer
PRINT_BED_WIDTH_MM = 225  # Default: Elegoo Neptune 4 Pro
PRINT_BED_DEPTH_MM = 225  # Default: Elegoo Neptune 4 Pro

# Derived constants (calculated from print bed size)
MAX_GRIDFINITY_UNITS_X = PRINT_BED_WIDTH_MM // GRIDFINITY_UNIT_MM  # 5 units
MAX_GRIDFINITY_UNITS_Y = PRINT_BED_DEPTH_MM // GRIDFINITY_UNIT_MM  # 5 units


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
