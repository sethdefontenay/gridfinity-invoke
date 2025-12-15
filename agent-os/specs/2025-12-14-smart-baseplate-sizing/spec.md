# Specification: Drawer Fit Solution

## Goal
Generate a complete drawer-fit solution from physical drawer dimensions (mm), automatically creating an optimally-sized baseplate and all necessary spacers to fill gaps and center the baseplate within the drawer.

## User Stories
- As a gridfinity user, I want to enter my drawer dimensions in millimeters so that I can get a perfectly fitted baseplate and spacer set without manual calculations
- As a maker, I want print-optimized output (half-set of spacers) so that I can efficiently print the spacers with proper interlocking alignment features
- As a user with large drawers, I want to be prompted to split oversized baseplates so that I can print pieces that fit on my print bed

## Specific Requirements

**New invoke task `drawer-fit`**
- Create new task separate from existing `baseplate` task
- Accept `--width` (X dimension) and `--depth` (Y dimension) parameters in millimeters
- Follow existing task patterns: JSON docstring format, hyphenated task name, colored output helpers
- Default output path pattern: `output/drawer-fit-baseplate.stl` and `output/drawer-fit-spacers.stl`
- Task signature: `@task` decorator with `name="drawer-fit"` for hyphenated CLI name

**Dimension calculation and validation**
- Convert mm to gridfinity units using 1 unit = 42mm formula
- Round down (floor) to guarantee fit - conservative approach
- Minimum valid input: 42mm in each dimension (produces at least 1x1 baseplate)
- Validate inputs are positive numbers; error with `print_error` + `sys.exit(1)` if invalid
- Error clearly if dimensions too small to produce any gridfinity units

**Calculation summary output**
- Display input drawer dimensions (width x depth in mm)
- Display resulting gridfinity units (width x depth units)
- Display actual baseplate dimensions (units * 42mm)
- Display gap dimensions on each side (mm)
- Display which spacers will be generated (corner, front/back, left/right based on 4mm threshold)

**Print bed configuration**
- Add module-level constants to `generators.py` for print bed configuration
- `PRINT_BED_WIDTH_MM = 225` (default: Elegoo Neptune 4 Pro)
- `PRINT_BED_DEPTH_MM = 225` (default: Elegoo Neptune 4 Pro)
- Calculate derived constants: `MAX_GRIDFINITY_UNITS_X = PRINT_BED_WIDTH_MM // 42` (yields 5)
- Calculate derived constants: `MAX_GRIDFINITY_UNITS_Y = PRINT_BED_DEPTH_MM // 42` (yields 5)
- User can edit these constants once to change defaults for their printer
- All print bed warning logic uses these constants instead of hardcoded values

**Print bed constraint warnings**
- If calculated baseplate exceeds `MAX_GRIDFINITY_UNITS_X` or `MAX_GRIDFINITY_UNITS_Y`, display warning using `print_warning` helper
- Suggest how to split baseplate into multiple pieces that fit the print bed
- Split suggestion algorithm: divide larger dimension by max units, show resulting piece sizes
- Check spacers against `PRINT_BED_WIDTH_MM`/`PRINT_BED_DEPTH_MM` limit; warn if any spacer piece exceeds limit

**Interactive baseplate splitting**
- After displaying oversized warning and split suggestion, prompt user: "Split into smaller baseplates? [Y/n]: "
- Use existing `prompt_with_default` pattern but with "Y" as default (pressing Enter accepts split)
- Accept "y", "Y", "yes", "" (empty/Enter) as affirmative; "n", "N", "no" as negative
- If user declines, proceed with generating single oversized baseplate (current behavior)

**Baseplate split calculation**
- For X overflow: divide units_x by MAX_GRIDFINITY_UNITS_X, create list of piece widths
- For Y overflow: divide units_y by MAX_GRIDFINITY_UNITS_Y, create list of piece depths
- If both overflow: create a grid of baseplates (X pieces * Y pieces total)
- Each piece size: full MAX units except final piece gets remainder
- Example: 12 units with max 5 -> [5, 5, 2] (three pieces)

**Split baseplate generation**
- Generate each baseplate piece as separate STL file
- Naming pattern: `baseplate-1.stl`, `baseplate-2.stl`, etc. (numbered sequentially)
- When project active: `{component-name}-baseplate-1.stl`, `{component-name}-baseplate-2.stl`, etc.
- Display summary of generated pieces with their sizes (e.g., "Generated baseplate-1.stl (5x5 units)")
- Generate spacers once for the full drawer dimensions (spacers don't need splitting)

**GridfinityDrawerSpacer integration**
- Import and use `GridfinityDrawerSpacer` from cqgridfinity library
- Instantiate with `dr_width` (X) and `dr_depth` (Y) parameters from user input
- Use `render_half_set()` method for print-optimized spacer output
- Spacers include interlocking jigsaw pegs/holes for alignment (handled by library)
- Spacers only generated when gap >= 4mm (cqgridfinity's internal threshold)

**STL file generation**
- Generate two STL files when not splitting: baseplate and spacer half-set
- Generate multiple STL files when splitting: numbered baseplates and spacer half-set
- Use `GridfinityBaseplate` for baseplate (same as existing `generate_baseplate`)
- Use `GridfinityDrawerSpacer.render_half_set()` for spacers
- Create parent directories if needed (follow existing pattern)
- Export using `.val().exportStl()` pattern from existing generators

**Project integration**
- Check for active project using `get_active_project()`
- When project active: prompt for component name using `prompt_with_default`
- Default component name format: `drawer-fit-{width}x{depth}mm`
- Save all STL files (single or split baseplates + spacers) to project directory
- Add component to config with type `drawer-fit` and all relevant metadata (width_mm, depth_mm, units_width, units_depth, split_count if applicable)
- When no project: save to output directory with default filenames

**Generator function architecture**
- Add new `generate_drawer_fit` function to `generators.py`
- Add new `generate_split_baseplates` function for multi-piece generation
- Return a dict or namedtuple with paths and calculation metadata
- Keep calculation logic in generator for testability
- Task handles only user interaction and output formatting

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**Existing `baseplate` task in `tasks.py` (lines 249-305)**
- Reuse exact task structure pattern: imports, validation, project detection, output formatting
- Reuse colored output helpers: `print_header`, `print_success`, `print_error`
- Reuse `prompt_with_default` for component naming and split confirmation
- Follow same error handling pattern: `print_error` then `sys.exit(1)`
- Add new `print_warning` helper for print bed warnings (yellow color)

**Existing `generate_baseplate` in `generators.py`**
- Reuse directory creation pattern: `output_path.parent.mkdir(parents=True, exist_ok=True)`
- Reuse STL export pattern: `result.val().exportStl(str(output_path))`
- Use `GridfinityBaseplate` from cqgridfinity for baseplate generation
- Call multiple times with different dimensions for split baseplates

**Project functions in `projects.py`**
- Use `get_active_project()` to check for active project
- Use `get_project_path()` to get output directory for project
- Use `add_component_to_config()` to save component metadata
- Follow existing component dict structure with `name`, `type`, and dimension fields

**JSON docstring format from existing tasks**
- Follow format: `{"desc": "...", "params": [...], "returns": {}}`
- Each param has: `name`, `type`, `desc`, `example` fields

## Out of Scope
- Modifying the existing `baseplate` task
- Support for inches or other unit systems (mm only)
- Full spacer set output (only half-set for print optimization)
- Custom spacer configurations (auto-generation only)
- Manual override of which spacers to include
- Support for asymmetric unit inputs (e.g., width in mm, depth in units)
- Configurable rounding mode (always round down)
- Interactive mode for dimension entry
- Preview/dry-run mode without generating files
- Separate tasks for baseplate-only or spacers-only generation
- Full config file system for print bed size (simple module constants only)
