# Task Breakdown: Drawer Fit Solution

## Overview
Total Tasks: 21 (across 4 task groups)

This spec enables users to enter drawer dimensions in millimeters and automatically generate a complete drawer-fit solution: an optimally-sized baseplate and all necessary spacers to fill gaps and center the baseplate within the drawer.

## Task List

### Core Module

#### Task Group 1: Drawer Fit Generator Function
**Dependencies:** None

- [ ] 1.0 Complete drawer fit generator module
  - [ ] 1.1 Write 4-6 focused tests for drawer fit calculations and generation
    - Test mm to gridfinity unit conversion (e.g., 100mm -> 2 units, 84mm actual)
    - Test floor rounding behavior (e.g., 125mm -> 2 units, not 3)
    - Test minimum dimension validation (< 42mm should raise error)
    - Test gap calculations (e.g., 100mm drawer, 2 units = 84mm, gap = 16mm total)
    - Test that baseplate STL file is created at expected path
    - Skip exhaustive edge case testing
  - [ ] 1.2 Add print bed configuration constants to `generators.py`
    - Add `PRINT_BED_WIDTH_MM = 225` (default: Elegoo Neptune 4 Pro)
    - Add `PRINT_BED_DEPTH_MM = 225` (default: Elegoo Neptune 4 Pro)
    - Add `MAX_GRIDFINITY_UNITS_X = PRINT_BED_WIDTH_MM // 42` (calculated, yields 5)
    - Add `MAX_GRIDFINITY_UNITS_Y = PRINT_BED_DEPTH_MM // 42` (calculated, yields 5)
    - Add comment explaining user can edit these values for their printer
    - Place constants at top of module after imports
  - [ ] 1.3 Add `print_warning` helper function to `tasks.py`
    - Follow existing pattern: `print_warning(message: str) -> None`
    - Use yellow color: `f"{Fore.YELLOW}{message}{Style.RESET_ALL}"`
    - Place alongside existing `print_header`, `print_success`, `print_error`
  - [ ] 1.4 Create `generate_drawer_fit` function in `generators.py`
    - Signature: `generate_drawer_fit(width_mm: float, depth_mm: float, baseplate_path: Path, spacer_path: Path) -> DrawerFitResult`
    - Define `DrawerFitResult` as NamedTuple with fields:
      - `baseplate_path: Path`
      - `spacer_path: Path | None` (None if no spacers needed)
      - `units_width: int`
      - `units_depth: int`
      - `actual_width_mm: float`
      - `actual_depth_mm: float`
      - `gap_x_mm: float` (total gap in X direction)
      - `gap_y_mm: float` (total gap in Y direction)
    - Convert mm to units: `units = int(mm // 42)` (floor division)
    - Validate minimum: raise `ValueError` if either dimension < 42mm
    - Calculate actual dimensions: `actual_mm = units * 42`
    - Calculate gaps: `gap_mm = input_mm - actual_mm`
  - [ ] 1.5 Implement baseplate generation in `generate_drawer_fit`
    - Import and use `GridfinityBaseplate` from cqgridfinity
    - Create baseplate with calculated units
    - Export using `.val().exportStl()` pattern
    - Create parent directories with `output_path.parent.mkdir(parents=True, exist_ok=True)`
  - [ ] 1.6 Implement spacer generation in `generate_drawer_fit`
    - Import `GridfinityDrawerSpacer` from cqgridfinity
    - Instantiate with `dr_width=width_mm` and `dr_depth=depth_mm`
    - Use `render_half_set()` method for print-optimized output
    - Only generate spacers if gap >= 4mm (cqgridfinity threshold)
    - Set `spacer_path` to None if no spacers generated
  - [ ] 1.7 Ensure generator tests pass
    - Run ONLY the 4-6 tests from 1.1
    - Verify calculations are correct
    - Verify both STL files are created when expected

**Acceptance Criteria:**
- Tests from 1.1 pass
- Print bed config constants defined and calculated correctly
- `generate_drawer_fit` correctly converts mm to gridfinity units
- Floor rounding ensures baseplate always fits
- Gap calculations are accurate
- Both baseplate and spacer STL files generated correctly
- Spacers only generated when gap >= 4mm

---

### Invoke Task

#### Task Group 2: Drawer Fit Invoke Task
**Dependencies:** Task Group 1

- [ ] 2.0 Complete drawer-fit invoke task
  - [ ] 2.1 Write 4-6 focused tests for drawer-fit task
    - Test task accepts `--width` and `--depth` parameters
    - Test task displays calculation summary (input mm, result units, actual mm, gaps)
    - Test task outputs warning when baseplate exceeds max units (from config constants)
    - Test task generates both STL files in correct location
    - Test task fails with error for invalid dimensions (< 42mm)
    - Skip testing all output formatting details
  - [ ] 2.2 Create `drawer_fit` task in `tasks.py`
    - Use `@task(name="drawer-fit")` decorator for hyphenated CLI name
    - Parameters: `width: float`, `depth: float`, `output: str = "output/drawer-fit"`
    - JSON docstring format matching existing tasks
    - Import `generate_drawer_fit` from generators
    - Import print bed config constants from generators
  - [ ] 2.3 Implement input validation
    - Validate both dimensions are positive numbers
    - Validate both dimensions >= 42mm (minimum for 1x1 baseplate)
    - Use `print_error` + `sys.exit(1)` for validation failures
    - Clear error messages explaining minimum requirements
  - [ ] 2.4 Implement calculation summary output
    - Display input drawer dimensions: "Drawer: {width} x {depth} mm"
    - Display gridfinity units: "Units: {units_width} x {units_depth}"
    - Display actual baseplate size: "Baseplate: {actual_width} x {actual_depth} mm"
    - Display gap per side: "Gaps: X={gap_x/2}mm per side, Y={gap_y/2}mm per side"
    - Display which spacers will be generated (based on 4mm threshold)
  - [ ] 2.5 Implement print bed constraint warnings using config constants
    - Import `PRINT_BED_WIDTH_MM`, `PRINT_BED_DEPTH_MM`, `MAX_GRIDFINITY_UNITS_X`, `MAX_GRIDFINITY_UNITS_Y` from generators
    - Use `print_warning` if baseplate exceeds `MAX_GRIDFINITY_UNITS_X` or `MAX_GRIDFINITY_UNITS_Y`
    - Display split suggestion using calculated max units
    - Check spacers against `PRINT_BED_WIDTH_MM`/`PRINT_BED_DEPTH_MM` and warn if exceeded
    - Still proceed with generation after warning
  - [ ] 2.6 Ensure drawer-fit task tests pass
    - Run ONLY the 4-6 tests from 2.1
    - Verify CLI accepts parameters correctly
    - Verify output messages are displayed

**Acceptance Criteria:**
- Tests from 2.1 pass
- `invoke drawer-fit --width=500 --depth=400` works correctly
- Calculation summary displays all required information
- Print bed warnings use configurable constants (not hardcoded values)
- Print bed warnings appear for oversized baseplates
- Clear error messages for invalid input

---

### Project Integration

#### Task Group 3: Project-Aware Drawer Fit
**Dependencies:** Task Group 2

- [ ] 3.0 Complete project integration for drawer-fit task
  - [ ] 3.1 Write 3-5 focused tests for project integration
    - Test drawer-fit with active project prompts for component name
    - Test drawer-fit saves both STL files to project directory
    - Test drawer-fit adds component to config with type "drawer-fit"
    - Test drawer-fit without active project uses default output directory
    - Skip testing all config field combinations
  - [ ] 3.2 Add project detection to drawer-fit task
    - Import `get_active_project`, `get_project_path`, `add_component_to_config` from projects
    - Check `get_active_project()` at start of task
    - Branch logic based on whether project is active
  - [ ] 3.3 Implement project-aware output paths
    - When project active: use `get_project_path(active_project)`
    - Default component name format: `drawer-fit-{width}x{depth}mm`
    - Prompt user with `prompt_with_default("Name", default_name)`
    - Save baseplate to: `projects/<project>/<name>-baseplate.stl`
    - Save spacers to: `projects/<project>/<name>-spacers.stl`
  - [ ] 3.4 Implement component config entry
    - Component dict structure:
      ```python
      {
          "name": component_name,
          "type": "drawer-fit",
          "width_mm": width,
          "depth_mm": depth,
          "units_width": result.units_width,
          "units_depth": result.units_depth,
      }
      ```
    - Call `add_component_to_config(active_project, component)`
    - Display success message: "Added to project: {active_project}"
  - [ ] 3.5 Ensure project integration tests pass
    - Run ONLY the 3-5 tests from 3.1
    - Verify project-aware behavior works correctly
    - Verify config.json is updated

**Acceptance Criteria:**
- Tests from 3.1 pass
- With active project: prompts for name, saves to project directory, updates config
- Without active project: saves to `output/` directory with default names
- Component entry includes all relevant metadata

---

### Testing

#### Task Group 4: Test Review and Final Validation
**Dependencies:** Task Groups 1-3

- [ ] 4.0 Review and validate complete implementation
  - [ ] 4.1 Review all tests from Task Groups 1-3
    - 4-6 tests from Task Group 1 (generator function)
    - 4-6 tests from Task Group 2 (invoke task)
    - 3-5 tests from Task Group 3 (project integration)
    - Total: approximately 11-17 tests
  - [ ] 4.2 Analyze test coverage gaps for drawer-fit feature
    - Identify critical end-to-end workflows lacking coverage
    - Focus ONLY on gaps related to this spec's requirements
    - Prioritize integration between calculation, generation, and project management
  - [ ] 4.3 Write up to 5 additional integration tests if needed
    - Test full workflow: drawer dimensions -> calculation -> STL generation
    - Test project workflow: new-project -> drawer-fit -> load (regenerates correctly)
    - Test edge case: exactly 42mm input produces 1x1 baseplate
    - Test warning workflow: oversized drawer triggers warning but still generates
    - Skip edge cases and error scenarios beyond critical paths
  - [ ] 4.4 Run feature-specific tests only
    - Run ONLY tests related to drawer-fit feature
    - Expected total: approximately 16-22 tests maximum
    - Verify all critical workflows pass
    - Do NOT run entire application test suite

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 16-22 tests total)
- Full workflow from drawer dimensions to STL files works end-to-end
- Project integration works correctly with `load` task
- No more than 5 additional tests added when filling gaps
- Testing focused exclusively on drawer-fit requirements

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Drawer Fit Generator Function** - Core calculation and generation logic needed by task
2. **Task Group 2: Drawer Fit Invoke Task** - CLI interface depends on generator from Group 1
3. **Task Group 3: Project Integration** - Project awareness depends on working task from Group 2
4. **Task Group 4: Final Validation** - Integration testing after all components exist

## Key Implementation Notes

### TDD Approach
- Write tests BEFORE or alongside implementation
- NO stubs, mocks of core functionality, or dummy implementations
- Tests must exercise real functionality
- Use temporary directories for test isolation

### JSON Docstring Format
The drawer-fit task must use this format (existing pattern from tasks.py):
```python
@task(name="drawer-fit")
def drawer_fit(ctx: Context, width: float, depth: float, output: str = "output/drawer-fit") -> None:
    """
    {
        "desc": "Generate a complete drawer-fit solution from drawer dimensions",
        "params": [
            {"name": "width", "type": "float", "desc": "Drawer width (X dimension) in millimeters", "example": "500"},
            {"name": "depth", "type": "float", "desc": "Drawer depth (Y dimension) in millimeters", "example": "400"}
        ],
        "returns": {}
    }
    """
```

### Constants
```python
# Gridfinity standard
GRIDFINITY_UNIT_MM = 42  # 1 gridfinity unit = 42mm
MIN_SPACER_GAP_MM = 4    # cqgridfinity threshold for spacer generation

# Print bed configuration - edit these values for your printer
PRINT_BED_WIDTH_MM = 225   # Default: Elegoo Neptune 4 Pro
PRINT_BED_DEPTH_MM = 225   # Default: Elegoo Neptune 4 Pro

# Derived constants (calculated from print bed size)
MAX_GRIDFINITY_UNITS_X = PRINT_BED_WIDTH_MM // 42  # 5 units for 225mm bed
MAX_GRIDFINITY_UNITS_Y = PRINT_BED_DEPTH_MM // 42  # 5 units for 225mm bed
```

### File Structure (New/Modified Files)
```
gridfinity/
├── tasks.py                        # MODIFIED: Add drawer-fit task, add print_warning helper
└── src/
    └── gridfinity_invoke/
        └── generators.py           # MODIFIED: Add generate_drawer_fit function, DrawerFitResult, print bed config constants
```

### Existing Code to Leverage
- `print_header()`, `print_success()`, `print_error()` from tasks.py
- `prompt_with_default()` from tasks.py
- `generate_baseplate()` pattern from generators.py
- `GridfinityBaseplate` from cqgridfinity
- `GridfinityDrawerSpacer` from cqgridfinity (new import)
- Project functions: `get_active_project()`, `get_project_path()`, `add_component_to_config()`
- Directory creation pattern: `Path.parent.mkdir(parents=True, exist_ok=True)`
- STL export pattern: `result.val().exportStl(str(output_path))`

### Print Bed Warning Example Output
```
Warning: Calculated baseplate (7x6 units = 294x252mm) exceeds print bed (225x225mm)
   Suggestion: Split into 2 baseplates: 5x6 + 2x6 units

Proceeding with generation...
```

### Component Config Entry Format
```json
{
  "name": "drawer-fit-500x400mm",
  "type": "drawer-fit",
  "width_mm": 500,
  "depth_mm": 400,
  "units_width": 11,
  "units_depth": 9
}
```
