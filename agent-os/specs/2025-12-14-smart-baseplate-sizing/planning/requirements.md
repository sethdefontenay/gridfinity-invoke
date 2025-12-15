# Spec Requirements: Drawer Fit Solution (Smart Drawer Baseplate)

## Initial Description
Allow users to provide physical dimensions (width and length in mm) of a space they want to fill. The tool calculates how many gridfinity units fit in each direction (1 gridfinity unit = 42mm) and automatically creates a baseplate of that size.

## Updated Description (Scope Change)
Generate a complete drawer-fit solution from drawer dimensions (width and depth in mm). The tool will:
1. Calculate how many gridfinity units fit in each direction
2. Generate an appropriately sized baseplate
3. Generate all necessary drawer spacers (corner, front/back, left/right) to fill gaps and center the baseplate
4. Prompt to split oversized baseplates into printable pieces

This expanded scope leverages cqgridfinity's `GridfinityDrawerSpacer` class which handles all calculations and spacer generation automatically.

## Requirements Discussion

### First Round Questions

**Q1:** I assume this will be a new invoke task (e.g., `invoke baseplate-from-mm` or `invoke smart-baseplate`) separate from the existing `baseplate` task. Is that correct, or should we extend/modify the existing `baseplate` task to accept mm dimensions as an alternative input mode?
**Answer:** New task (separate from existing `baseplate` task)

**Q2:** For leftover space (when dimensions don't divide evenly by 42mm), I'm thinking we should round down to the largest fitting baseplate (e.g., 100mm input becomes 2 units = 84mm actual). Should we round down (conservative), round to nearest, or provide both options via a flag?
**Answer:** Round down (conservative, guaranteed to fit)

**Q3:** I assume we should display a helpful summary showing the calculation result before generating. Is that level of detail helpful, or should we keep output minimal?
**Answer:** Yes, show calculation summary (input mm, result units, actual mm, gaps)

**Q4:** Should we support asymmetric inputs where users might say "width in mm, length in units" for when they already know one dimension? Or keep it simple with both inputs in the same unit (mm)?
**Answer:** Keep simple - both inputs must be in mm only

**Q5:** Should this task integrate with the project save/load system the same way the existing `baseplate` task does (prompt for component name when a project is active, save to project config)?
**Answer:** Yes, integrate with project save/load system (same as existing baseplate task)

**Q6:** Is there anything that should explicitly be excluded from this feature? For example: should we NOT support input in inches or other units at this time?
**Answer:** mm only - no inches or other units at this time

### Scope Update (Post-Research)

After researching cqgridfinity capabilities, the scope expanded significantly:

**Original Scope:** Simple mm-to-units conversion + baseplate generation

**New Scope:** Complete drawer-fit solution using `GridfinityDrawerSpacer`:
- Baseplate generation sized to fit drawer
- Automatic spacer generation to fill gaps and center the baseplate
- Spacers include interlocking alignment features (jigsaw pegs/holes)
- Print-optimized output using `render_half_set()` (user prints twice)

### Existing Code to Reference

**Similar Features Identified:**
- Feature: Existing baseplate task - Path: `/home/seth/tools/gridfinity/tasks.py` (lines 249-305)
- Components to potentially reuse: Task structure, colored output helpers, project integration pattern
- Backend logic to reference: `generate_baseplate` from `gridfinity_invoke.generators`, project functions from `gridfinity_invoke.projects`

**New Library Integration:**
- cqgridfinity `GridfinityDrawerSpacer` class
- Parameters: `dr_width` (X dimension), `dr_depth` (Y dimension) in mm
- Method: `render_half_set()` for print-optimized spacer output

### Follow-up Questions
No follow-up questions were needed.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements
- New invoke task for creating complete drawer-fit solutions from millimeter dimensions
- Accept drawer width (X) and depth (Y) inputs in millimeters (mm)
- Use cqgridfinity's `GridfinityDrawerSpacer` for calculations and generation
- Calculate gridfinity units that fit in drawer
- Display calculation summary showing:
  - Input drawer dimensions (mm)
  - Resulting gridfinity units (width x depth)
  - Actual baseplate dimensions (mm)
  - Gap dimensions on each side (mm)
  - Which spacers will be generated (based on 4mm minimum gap threshold)
- Generate multiple STL files:
  - Baseplate STL (or multiple numbered baseplates if split)
  - Spacer half-set STL (user prints twice for complete set)
- Display spacer information (which spacers needed: corner, front/back, left/right)
- Integrate with project save/load system when a project is active

### Print Bed Configuration

**Default Printer:** Elegoo Neptune 4 Pro
**Default Max Print Size:** 225 x 225 mm
**Default Max Gridfinity Units:** 5 x 5 units (210 x 210 mm)

**Configurable Constants (in `generators.py`):**
```python
# Print bed configuration - edit these values for your printer
PRINT_BED_WIDTH_MM = 225   # Default: Elegoo Neptune 4 Pro
PRINT_BED_DEPTH_MM = 225   # Default: Elegoo Neptune 4 Pro

# Derived constants (calculated from print bed size)
MAX_GRIDFINITY_UNITS_X = PRINT_BED_WIDTH_MM // 42  # 5 units for 225mm bed
MAX_GRIDFINITY_UNITS_Y = PRINT_BED_DEPTH_MM // 42  # 5 units for 225mm bed
```

**Configuration Approach:**
- Simple module-level constants that user can edit once
- No full config file system needed
- Derived max unit values calculated automatically from bed size

### Baseplate Handling (Oversized)

**Warning Display:**
- If calculated baseplate exceeds max units in either dimension, display a warning
- Suggest how to split the baseplate into multiple pieces

**Interactive Splitting:**
- After warning, prompt user: "Split into smaller baseplates? [Y/n]: "
- Default is Yes (pressing Enter accepts split)
- If user accepts: generate multiple numbered baseplate STL files
- If user declines: generate single oversized baseplate with warning

**Split Calculation Algorithm:**
- For X overflow: divide by MAX_GRIDFINITY_UNITS_X, create piece list
- For Y overflow: divide by MAX_GRIDFINITY_UNITS_Y, create piece list
- If both overflow: create grid of baseplates (X pieces * Y pieces)
- Each piece gets MAX units except final piece gets remainder

**Example - 530x247mm drawer (12x5 units) with 5x5 max:**
- X needs split: 12 -> [5, 5, 2] (3 pieces)
- Y fits: 5 -> [5] (1 piece)
- Result: 3 baseplates total: 5x5, 5x5, 2x5 units
- Files: baseplate-1.stl (5x5), baseplate-2.stl (5x5), baseplate-3.stl (2x5)

**Example - 420x420mm drawer (10x10 units) with 5x5 max:**
- X needs split: 10 -> [5, 5] (2 pieces)
- Y needs split: 10 -> [5, 5] (2 pieces)
- Result: 4 baseplates total (2x2 grid): 5x5, 5x5, 5x5, 5x5 units
- Files: baseplate-1.stl through baseplate-4.stl (all 5x5)

**Output Example (with splitting):**
```
Warning: Calculated baseplate (12x5 units = 504x210mm) exceeds print bed (225x225mm)
   Suggestion: Split into 3 baseplates: 5x5 + 5x5 + 2x5 units

Split into smaller baseplates? [Y/n]:

Generating split baseplates...
  Generated baseplate-1.stl (5x5 units)
  Generated baseplate-2.stl (5x5 units)
  Generated baseplate-3.stl (2x5 units)
```

**Output Example (declining split):**
```
Warning: Calculated baseplate (12x5 units = 504x210mm) exceeds print bed (225x225mm)
   Suggestion: Split into 3 baseplates: 5x5 + 5x5 + 2x5 units

Split into smaller baseplates? [Y/n]: n

Proceeding with single oversized baseplate...
  Generated drawer-fit-baseplate.stl (12x5 units) - WARNING: exceeds print bed
```

**Spacer Handling:**
- Spacers should also respect the configured print bed limits
- If any spacer piece exceeds the limit, warn and suggest alternatives

### Reusability Opportunities
- Reuse existing `baseplate` task pattern from `tasks.py`
- Reuse project integration functions: `get_active_project`, `get_project_path`, `add_component_to_config`, `set_active_project`
- Reuse colored output helpers: `print_header`, `print_success`, `print_error`
- Add new `print_warning` helper for print bed warnings
- Reuse `prompt_with_default` for component naming and split confirmation
- Leverage cqgridfinity's `GridfinityDrawerSpacer` for all calculations and spacer geometry

### Scope Boundaries
**In Scope:**
- New invoke task accepting drawer mm dimensions
- Conversion calculation (mm to gridfinity units)
- Baseplate generation sized to fit drawer
- Spacer generation using `GridfinityDrawerSpacer`
- Auto-detect which spacers are needed (4mm minimum gap threshold)
- Print-optimized half-set output (user prints twice)
- Calculation and spacer summary output
- Multiple STL file output (baseplate + spacer half-set)
- Project integration (same behavior as existing baseplate task)
- Print bed size warnings with split suggestions
- Configurable print bed size via module-level constants
- Interactive prompt-based baseplate splitting when oversized
- Multiple numbered baseplate STL generation for split baseplates

**Out of Scope:**
- Modifying the existing `baseplate` task
- Support for inches or other unit systems
- Full spacer set output (only half-set for print optimization)
- Custom spacer configurations (auto-generation only)
- Manual override of which spacers to include
- Full config file system for print bed size (simple module constants only)

### Technical Considerations
- 1 gridfinity unit = 42mm (standard gridfinity specification)
- Minimum valid input: 42mm in each dimension (to produce at least 1x1 baseplate)
- Should validate inputs are positive numbers
- Should warn/error if input is too small to produce any units
- Spacers only generated when gap >= 4mm (cqgridfinity threshold)
- Spacers include interlocking jigsaw pegs/holes for alignment
- `render_half_set()` produces one of each unique spacer type needed
- Task naming convention should follow existing patterns (hyphenated task names)
- JSON docstring format for task help (matching existing tasks)
- Follow existing error handling patterns (print_error + sys.exit(1))
- Output file naming: `drawer-fit-baseplate.stl` (single) or `baseplate-1.stl`, `baseplate-2.stl`, etc. (split)
- Print bed size configurable via module constants in `generators.py`
- Max gridfinity units calculated from print bed size: `bed_size // 42`
- Split prompt uses "Y" as default (Enter accepts split)
