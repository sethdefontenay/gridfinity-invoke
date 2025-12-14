# Specification: Drawer Fit Solution

## Goal
Generate a complete drawer-fit solution from physical drawer dimensions (mm), automatically creating an optimally-sized baseplate and all necessary spacers to fill gaps and center the baseplate within the drawer.

## User Stories
- As a gridfinity user, I want to enter my drawer dimensions in millimeters so that I can get a perfectly fitted baseplate and spacer set without manual calculations
- As a maker, I want print-optimized output (half-set of spacers) so that I can efficiently print the spacers with proper interlocking alignment features

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
- Still generate the oversized STL but warn user it won't fit on print bed
- Let user decide whether to proceed or manually adjust dimensions
- Check spacers against `PRINT_BED_WIDTH_MM`/`PRINT_BED_DEPTH_MM` limit; warn if any spacer piece exceeds limit

**GridfinityDrawerSpacer integration**
- Import and use `GridfinityDrawerSpacer` from cqgridfinity library
- Instantiate with `dr_width` (X) and `dr_depth` (Y) parameters from user input
- Use `render_half_set()` method for print-optimized spacer output
- Spacers include interlocking jigsaw pegs/holes for alignment (handled by library)
- Spacers only generated when gap >= 4mm (cqgridfinity's internal threshold)

**STL file generation**
- Generate two STL files: baseplate and spacer half-set
- Use `GridfinityBaseplate` for baseplate (same as existing `generate_baseplate`)
- Use `GridfinityDrawerSpacer.render_half_set()` for spacers
- Create parent directories if needed (follow existing pattern)
- Export using `.val().exportStl()` pattern from existing generators

**Project integration**
- Check for active project using `get_active_project()`
- When project active: prompt for component name using `prompt_with_default`
- Default component name format: `drawer-fit-{width}x{depth}mm`
- Save both STL files to project directory
- Add component to config with type `drawer-fit` and all relevant metadata (width_mm, depth_mm, units_width, units_depth)
- When no project: save to output directory with default filenames

**Generator function architecture**
- Add new `generate_drawer_fit` function to `generators.py`
- Return a dict or namedtuple with paths and calculation metadata
- Keep calculation logic in generator for testability
- Task handles only user interaction and output formatting

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**Existing `baseplate` task in `tasks.py` (lines 249-305)**
- Reuse exact task structure pattern: imports, validation, project detection, output formatting
- Reuse colored output helpers: `print_header`, `print_success`, `print_error`
- Reuse `prompt_with_default` for component naming
- Follow same error handling pattern: `print_error` then `sys.exit(1)`
- Add new `print_warning` helper for print bed warnings (yellow color)

**Existing `generate_baseplate` in `generators.py`**
- Reuse directory creation pattern: `output_path.parent.mkdir(parents=True, exist_ok=True)`
- Reuse STL export pattern: `result.val().exportStl(str(output_path))`
- Use `GridfinityBaseplate` from cqgridfinity for baseplate generation

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
- Automatic baseplate splitting (only warns and suggests, does not auto-split)
- Full config file system for print bed size (simple module constants only)
