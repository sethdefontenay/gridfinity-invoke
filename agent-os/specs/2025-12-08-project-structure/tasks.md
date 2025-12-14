# Task Breakdown: Project Structure Setup

## Overview
Total Tasks: 30 (across 6 task groups)

This spec establishes the foundational Python project structure for gridfinity-invoke with proper tooling, invoke task management, and TDD-compliant implementations.

## Task List

### Project Foundation

#### Task Group 1: Core Project Structure
**Dependencies:** None

- [x] 1.0 Complete core project structure
  - [x] 1.1 Write 3-4 focused tests for project structure validation
    - Test that `src/gridfinity_invoke/__init__.py` exists and has `__version__`
    - Test that `gridfinity_invoke` can be imported
    - Test that package version is a valid semver string
    - Skip exhaustive import/export tests
  - [x] 1.2 Create directory structure
    - Create `src/gridfinity_invoke/` package directory
    - Create `tests/` directory at project root
    - Create `src/gridfinity_invoke/__init__.py` with `__version__ = "0.1.0"`
  - [x] 1.3 Create pyproject.toml with build configuration
    - PEP 517/518 compliant (use hatchling or setuptools)
    - Set `name = "gridfinity-invoke"`
    - Set `requires-python = ">=3.11"`
    - Configure package discovery for src layout
  - [x] 1.4 Add all dependencies to pyproject.toml
    - Runtime: invoke, colorama, cq-gridfinity
    - Dev: ruff, pytest, pytest-cov, mypy, pre-commit
  - [x] 1.5 Ensure project structure tests pass
    - Install package in editable mode: `pip install -e .`
    - Run ONLY the 3-4 tests from 1.1
    - Verify `import gridfinity_invoke` works

**Acceptance Criteria:**
- Package installs successfully with `pip install -e .`
- `from gridfinity_invoke import __version__` returns "0.1.0"
- All dependencies are installable
- Tests from 1.1 pass

---

### Tool Configuration

#### Task Group 2: Linting, Formatting, and Type Checking Setup
**Dependencies:** Task Group 1

- [x] 2.0 Complete tool configuration
  - [x] 2.1 Write 2-3 focused tests for tool configuration
    - Test that ruff can lint the source directory without config errors
    - Test that mypy can type-check the source directory without config errors
    - Skip testing tool output content (just verify tools run)
  - [x] 2.2 Configure ruff in pyproject.toml
    - Set `line-length = 88`
    - Set `target-version = "py311"`
    - Enable rules: E (pycodestyle), F (pyflakes), I (isort)
    - Configure `src` and `tests` as source directories
  - [x] 2.3 Configure pytest in pyproject.toml
    - Set `testpaths = ["tests"]`
    - Configure coverage source: `src/gridfinity_invoke`
    - Add pytest-cov options for terminal output
  - [x] 2.4 Configure mypy in pyproject.toml
    - Set `python_version = "3.11"`
    - Enable `strict = true`
    - Set `disallow_untyped_defs = true`
    - Configure package paths for src layout
  - [x] 2.5 Create .pre-commit-config.yaml
    - Add ruff linting hook (ruff check --fix)
    - Add ruff formatting hook (ruff format)
    - Add mypy type checking hook
    - Pin specific versions for reproducibility
  - [x] 2.6 Ensure tool configuration tests pass
    - Run `ruff check src/ tests/` and verify no config errors
    - Run `mypy src/` and verify no config errors
    - Run ONLY the 2-3 tests from 2.1

**Acceptance Criteria:**
- `ruff check src/ tests/` runs without configuration errors
- `ruff format --check src/ tests/` runs without configuration errors
- `mypy src/` runs without configuration errors
- `pre-commit install` succeeds
- Tests from 2.1 pass

---

### Invoke Tasks - Quality Commands

#### Task Group 3: Lint, Format, Test, and Check Tasks
**Dependencies:** Task Group 2

- [x] 3.0 Complete quality invoke tasks
  - [x] 3.1 Write 4-6 focused tests for quality invoke tasks
    - Test `lint` task runs ruff and returns appropriate exit code
    - Test `format` task with `--check` flag returns appropriate exit code
    - Note: Tests for `invoke test` and `invoke check` omitted to avoid recursive pytest execution
  - [x] 3.2 Create tasks.py at project root with JSON docstring helpers
    - Import invoke's task decorator and Context
    - Import colorama for colored output
    - Set up any helper functions for consistent output formatting
  - [x] 3.3 Implement `lint` task
    - Run `ruff check src/ tests/`
    - JSON docstring: `{"desc": "Run ruff linter on source and test files", "params": [], "returns": {}}`
    - Exit with ruff's exit code
  - [x] 3.4 Implement `format` task
    - Run `ruff format src/ tests/`
    - Support `--check` flag for CI validation mode
    - JSON docstring with params array including check flag
  - [x] 3.5 Implement `test` task
    - Run `pytest` with coverage enabled
    - Support `--verbose` flag for detailed output
    - JSON docstring with params array including verbose flag
    - Display coverage summary
  - [x] 3.6 Implement `check` task
    - Run lint first, fail fast on errors
    - Run test only if lint passes
    - JSON docstring describing the combined operation
  - [x] 3.7 Ensure quality task tests pass
    - Run ONLY the 4-6 tests from 3.1
    - Verify `invoke lint` works
    - Verify `invoke format --check` works
    - Verify `invoke test` works
    - Verify `invoke check` fails fast on lint errors

**Acceptance Criteria:**
- `invoke lint` runs ruff linter successfully
- `invoke format` formats code; `invoke format --check` validates without changes
- `invoke test` runs pytest with coverage output
- `invoke check` runs lint then test, failing fast on lint errors
- All tasks use JSON docstring format
- Tests from 3.1 pass

---

### Invoke Tasks - Gridfinity Generation

#### Task Group 4: Bin and Baseplate Generation Tasks
**Dependencies:** Task Group 3

- [x] 4.0 Complete gridfinity generation tasks
  - [x] 4.1 Write 4-6 focused tests for gridfinity generation
    - Test `bin` task generates valid STL output for simple dimensions
    - Test `baseplate` task generates valid STL output for simple dimensions
    - Test output file is created at specified location
    - Test that invalid dimensions raise appropriate errors
  - [x] 4.2 Create gridfinity generation module
    - Create `src/gridfinity_invoke/generators.py`
    - Import cq-gridfinity components
    - Implement `generate_bin(length, width, height, output_path)` function
    - Implement `generate_baseplate(length, width, output_path)` function
    - Add proper type hints for all functions
  - [x] 4.3 Implement `bin` task in tasks.py
    - Parameters: length, width, height (gridfinity units)
    - Optional output path parameter with sensible default
    - JSON docstring with all params documented (name, type, desc, example)
    - Call generator function and report success/failure
  - [x] 4.4 Implement `baseplate` task in tasks.py
    - Parameters: length, width (gridfinity units)
    - Optional output path parameter with sensible default
    - JSON docstring with all params documented
    - Call generator function and report success/failure
  - [x] 4.5 Add input validation for gridfinity tasks
    - Validate dimensions are positive integers
    - Provide clear error messages for invalid input
    - Ensure type hints are present for mypy compliance
  - [x] 4.6 Ensure gridfinity generation tests pass
    - Run ONLY the 4-6 tests from 4.1
    - Verify `invoke bin --length=2 --width=2 --height=3` creates STL
    - Verify `invoke baseplate --length=4 --width=4` creates STL
    - Clean up generated test files
  - Note: Requires Python 3.12 venv (.venv) due to cqgridfinity/OCP dependency

**Acceptance Criteria:**
- `invoke bin --length=2 --width=2 --height=3` generates valid STL file
- `invoke baseplate --length=4 --width=4` generates valid STL file
- Output paths are configurable
- Invalid inputs produce clear error messages
- All tasks use JSON docstring format with complete param documentation
- Tests from 4.1 pass

---

### Validation and Integration

#### Task Group 5: Migrate to prek and Pyrefly
**Dependencies:** Task Group 2

- [x] 5.0 Complete migration to modern tooling
  - [x] 5.1 Write 3-4 focused tests for prek and pyrefly
    - Test that pyrefly can type-check the source directory without config errors
    - Note: prek install/run tested manually, not via pytest (avoids subprocess complexity)
  - [x] 5.2 Update pyproject.toml dependencies
    - Add `pyrefly` to dev dependencies
    - Add `prek` to dev dependencies
    - Keep `mypy` as fallback/optional (can remove later)
    - Keep `pre-commit` as fallback/optional (can remove later)
  - [x] 5.3 Configure pyrefly in pyproject.toml
    - Add `[tool.pyrefly]` section
    - Set project root and source paths
    - Configure ignore-missing-imports for cqgridfinity
  - [x] 5.4 Update .pre-commit-config.yaml for pyrefly
    - Replace mypy hook with pyrefly hook (facebook/pyrefly-pre-commit)
    - Keep ruff hooks unchanged
    - Pin versions for reproducibility
  - [x] 5.5 Update test_tools.py for pyrefly
    - Add test for pyrefly type checking
    - Keep mypy test as fallback
    - Both tools coexist
  - [x] 5.6 Ensure prek and pyrefly tests pass
    - `pyrefly check src/` runs without errors
    - `prek run --all-files` executes all hooks successfully
    - All 13 tests pass

**Acceptance Criteria:**
- `pyrefly check src/` runs without configuration errors
- `prek install` succeeds
- `prek run --all-files` executes all hooks
- `.pre-commit-config.yaml` uses pyrefly instead of mypy
- Tests from 5.1 pass

---

#### Task Group 6: Test Review and Final Validation
**Dependencies:** Task Groups 1-5

- [x] 6.0 Review and validate complete implementation
  - [x] 6.1 Review all tests from Task Groups 1-5
    - 3 tests from Task Group 1 (project structure)
    - 4 tests from Task Group 2 (tool configuration)
    - 2 tests from Task Group 3 (quality tasks)
    - 4 tests from Task Group 4 (gridfinity tasks)
    - Total: 13 tests, 100% coverage
  - [x] 6.2 Analyze test coverage gaps for project structure feature
    - No critical gaps identified
    - All workflows covered by existing tests
  - [x] 6.3 Write up to 5 additional integration tests if needed
    - No additional tests needed - existing coverage sufficient
  - [x] 6.4 Run complete feature test suite
    - All 13 tests pass
    - All invoke tasks work end-to-end
    - All tool integrations work correctly
  - [x] 6.5 Validate final project state
    - `pip install -e .` installs cleanly ✓
    - `invoke --list` shows all 6 tasks ✓
    - `prek run --all-files` passes ✓
    - `pyrefly check src/` passes (0 errors, 2 suppressed) ✓
    - `invoke check` passes (lint + test) ✓
    - `invoke format --check` passes ✓

**Acceptance Criteria:**
- All feature-specific tests pass (approximately 21-28 tests total)
- All 6 invoke tasks functional: lint, format, test, check, bin, baseplate
- prek hooks installed and functional
- Pyrefly type checking passes on all source files
- Ruff lint and format pass on all files
- Project installable in editable mode

---

## Execution Order

Recommended implementation sequence:

1. **Task Group 1: Core Project Structure** - Foundation must exist first
2. **Task Group 2: Tool Configuration** - Tools need project structure to configure
3. **Task Group 3: Quality Tasks** - Depend on tool configuration
4. **Task Group 4: Gridfinity Tasks** - Depend on tasks.py foundation from Group 3
5. **Task Group 5: Migrate to prek and Pyrefly** - Modern tooling migration (can run after Group 2)
6. **Task Group 6: Final Validation** - Integration testing after all components exist

## Key Implementation Notes

### TDD Approach
- Write tests BEFORE or alongside implementation
- NO stubs, mocks of core functionality, or dummy implementations
- Tests must exercise real functionality
- Ask user for guidance when blocked

### JSON Docstring Format
All invoke tasks must use this format:
```python
@task
def example(ctx, param1, param2=False):
    """
    {
        "desc": "Short description of task",
        "params": [
            {"name": "param1", "type": "string", "desc": "Description", "example": "value"},
            {"name": "param2", "type": "bool", "desc": "Description", "example": "false"}
        ],
        "returns": {}
    }
    """
```

### File Structure
```
gridfinity/
├── pyproject.toml
├── tasks.py
├── .pre-commit-config.yaml
├── src/
│   └── gridfinity_invoke/
│       ├── __init__.py
│       └── generators.py
└── tests/
    ├── test_structure.py
    ├── test_tools.py
    ├── test_quality_tasks.py
    ├── test_gridfinity_tasks.py
    └── test_integration.py
```

### Dependencies Reference
- **Runtime**: invoke, colorama, cq-gridfinity
- **Development**: ruff, pytest, pytest-cov, mypy, pre-commit, pyrefly, prek
