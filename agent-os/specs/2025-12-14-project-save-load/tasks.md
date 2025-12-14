# Task Breakdown: Project Save/Load System

## Overview
Total Tasks: 18 (across 4 task groups)

This spec enables users to organize Gridfinity designs into named projects with persistent configuration and automatic STL output management.

## Task List

### Project Management Core

#### Task Group 1: Project State and Configuration Module
**Dependencies:** None

- [ ] 1.0 Complete project state and configuration module
  - [ ] 1.1 Write 4-6 focused tests for project management
    - Test `get_active_project()` returns None when `.gridfinity-active` doesn't exist
    - Test `set_active_project(name)` creates `.gridfinity-active` with project name
    - Test `load_project_config(name)` reads and parses `config.json`
    - Test `save_project_config(name, config)` writes valid JSON to `config.json`
    - Test `add_component_to_config()` adds new component and updates duplicates by name
    - Skip exhaustive error handling tests
  - [ ] 1.2 Create project management module
    - Create `src/gridfinity_invoke/projects.py`
    - Import `pathlib.Path` and `json`
    - Define `PROJECTS_DIR = Path("projects")` constant
    - Define `ACTIVE_FILE = Path(".gridfinity-active")` constant
  - [ ] 1.3 Implement active project state functions
    - `get_active_project() -> str | None` - reads `.gridfinity-active` or returns None
    - `set_active_project(name: str) -> None` - writes project name to `.gridfinity-active`
    - Handle file not found gracefully
  - [ ] 1.4 Implement project configuration functions
    - `get_project_path(name: str) -> Path` - returns `projects/<name>/`
    - `load_project_config(name: str) -> dict` - reads and parses `config.json`
    - `save_project_config(name: str, config: dict) -> None` - writes `config.json`
    - `add_component_to_config(name: str, component: dict) -> None` - adds/updates component
  - [ ] 1.5 Ensure project management tests pass
    - Run ONLY the 4-6 tests from 1.1
    - Use temporary directories for isolation
    - Verify all file operations work correctly

**Acceptance Criteria:**
- Active project state persists across task invocations
- Config files are valid JSON
- Component deduplication works by name
- Tests from 1.1 pass

---

### Invoke Tasks - Project Commands

#### Task Group 2: New Project, Load, and List Tasks
**Dependencies:** Task Group 1

- [ ] 2.0 Complete project management invoke tasks
  - [ ] 2.1 Write 4-6 focused tests for project invoke tasks
    - Test `new-project` creates directory and config.json with correct structure
    - Test `new-project` sets newly created project as active
    - Test `new-project` fails with error if project already exists
    - Test `load` regenerates all STL files from config
    - Test `list-projects` shows all projects with active indicator
    - Test `list-projects` shows "No projects found" when empty
  - [ ] 2.2 Implement `new-project` task in tasks.py
    - Signature: `invoke new-project --name=<name>`
    - Create `projects/<name>/` directory
    - Write initial config: `{"name": "<name>", "components": []}`
    - Call `set_active_project(name)` to set as active
    - Fail with error if project already exists
    - Use JSON docstring format with params
  - [ ] 2.3 Implement `load` task in tasks.py
    - Signature: `invoke load --project=<name>`
    - Read config from `projects/<name>/config.json`
    - Loop through components and regenerate STL files
    - Call `set_active_project(name)` to set as active
    - Fail with error if project doesn't exist
    - Use JSON docstring format with params
  - [ ] 2.4 Implement `list-projects` task in tasks.py
    - Signature: `invoke list-projects`
    - List all directories under `projects/`
    - Mark active project with `*` indicator
    - Show "No projects found" if empty or doesn't exist
    - Use JSON docstring format
  - [ ] 2.5 Ensure project task tests pass
    - Run ONLY the 4-6 tests from 2.1
    - Verify `invoke new-project --name=test` works
    - Verify `invoke load --project=test` works
    - Verify `invoke list-projects` shows correct output

**Acceptance Criteria:**
- `invoke new-project --name=myproject` creates project and sets active
- `invoke load --project=myproject` regenerates all components
- `invoke list-projects` shows all projects with active marker
- All tasks use JSON docstring format
- Tests from 2.1 pass

---

### Modified Generation Tasks

#### Task Group 3: Project-Aware Bin and Baseplate Tasks
**Dependencies:** Task Group 2

- [ ] 3.0 Complete project-aware generation tasks
  - [ ] 3.1 Write 4-6 focused tests for modified generation tasks
    - Test `bin` with active project suggests default name like `bin-2x2x3`
    - Test `bin` saves to project directory and updates config
    - Test `bin` without active project uses existing `output/` behavior
    - Test `baseplate` with active project suggests default name like `baseplate-4x4`
    - Test `baseplate` saves to project directory and updates config
    - Test component name deduplication in config
  - [ ] 3.2 Create user prompt helper function
    - Add helper function for prompting with default value
    - Signature: `prompt_with_default(prompt: str, default: str) -> str`
    - Format: "Name [bin-2x2x3]: " where user can press Enter for default
    - Return user input or default if empty
  - [ ] 3.3 Modify `bin` task for project awareness
    - Check for active project via `get_active_project()`
    - If active: suggest default name `bin-{length}x{width}x{height}`
    - Prompt user to confirm or enter custom name
    - Save STL to `projects/<active>/<name>.stl`
    - Call `add_component_to_config()` with component data
    - If no active project: use existing behavior (save to `output/bin.stl`)
  - [ ] 3.4 Modify `baseplate` task for project awareness
    - Check for active project via `get_active_project()`
    - If active: suggest default name `baseplate-{length}x{width}`
    - Prompt user to confirm or enter custom name
    - Save STL to `projects/<active>/<name>.stl`
    - Call `add_component_to_config()` with component data
    - If no active project: use existing behavior (save to `output/baseplate.stl`)
  - [ ] 3.5 Ensure modified generation tests pass
    - Run ONLY the 4-6 tests from 3.1
    - Test with and without active project
    - Verify config.json updates correctly

**Acceptance Criteria:**
- `invoke bin` with active project prompts for name and saves to project
- `invoke baseplate` with active project prompts for name and saves to project
- Both tasks fall back to default behavior without active project
- Component entries added to config.json correctly
- Tests from 3.1 pass

---

### Testing

#### Task Group 4: Test Review and Final Validation
**Dependencies:** Task Groups 1-3

- [ ] 4.0 Review and validate complete implementation
  - [ ] 4.1 Review all tests from Task Groups 1-3
    - 4-6 tests from Task Group 1 (project management module)
    - 4-6 tests from Task Group 2 (project invoke tasks)
    - 4-6 tests from Task Group 3 (modified generation tasks)
    - Total: approximately 12-18 tests
  - [ ] 4.2 Analyze test coverage gaps for project save/load feature
    - Identify critical end-to-end workflows lacking coverage
    - Focus ONLY on gaps related to this spec's requirements
    - Prioritize integration between project management and generation
  - [ ] 4.3 Write up to 5 additional integration tests if needed
    - Test full workflow: new-project -> bin -> bin -> baseplate -> load
    - Test config persistence across task invocations
    - Test active project state persistence
    - Skip edge cases and error scenarios beyond critical paths
  - [ ] 4.4 Run feature-specific tests only
    - Run ONLY tests related to project save/load feature
    - Expected total: approximately 17-23 tests maximum
    - Verify all critical workflows pass
    - Do NOT run entire application test suite

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 17-23 tests total)
- Full workflow from project creation to load works end-to-end
- Active project state persists correctly
- No more than 5 additional tests added when filling gaps
- Testing focused exclusively on project save/load requirements

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Project State and Configuration Module** - Core functions needed by all other tasks
2. **Task Group 2: Project Commands** - New invoke tasks depend on module from Group 1
3. **Task Group 3: Modified Generation Tasks** - Depend on project management infrastructure
4. **Task Group 4: Final Validation** - Integration testing after all components exist

## Key Implementation Notes

### TDD Approach
- Write tests BEFORE or alongside implementation
- NO stubs, mocks of core functionality, or dummy implementations
- Tests must exercise real functionality
- Use temporary directories for test isolation

### JSON Docstring Format
All invoke tasks must use this format (existing pattern from tasks.py):
```python
@task
def new_project(ctx: Context, name: str) -> None:
    """
    {
        "desc": "Create a new Gridfinity project",
        "params": [
            {"name": "name", "type": "string", "desc": "Project name", "example": "my-project"}
        ],
        "returns": {}
    }
    """
```

### File Structure (New Files)
```
gridfinity/
├── .gridfinity-active              # NEW: Active project name
├── tasks.py                        # MODIFIED: Add project tasks, modify bin/baseplate
├── projects/                       # NEW: Project storage directory
│   └── <project-name>/
│       ├── config.json             # Project configuration
│       └── *.stl                   # Generated STL files
└── src/
    └── gridfinity_invoke/
        └── projects.py             # NEW: Project management module
```

### Config File Format
```json
{
  "name": "my-project",
  "components": [
    {"name": "main-bin", "type": "bin", "length": 2, "width": 2, "height": 3},
    {"name": "base", "type": "baseplate", "length": 4, "width": 4}
  ]
}
```

### Existing Code to Leverage
- `print_header()`, `print_success()`, `print_error()` from tasks.py
- `generate_bin()` and `generate_baseplate()` from generators.py
- JSON docstring format pattern from existing tasks
- `Path.parent.mkdir(parents=True, exist_ok=True)` pattern from generators.py
