# Specification: Project Structure Setup

## Goal
Establish the foundational Python project structure for gridfinity-invoke with invoke task management, ruff linting/formatting, pytest testing, mypy type checking, and pre-commit hooks, following TDD principles with real implementations only.

## User Stories
- As a developer, I want a well-organized src layout project structure so that tests are isolated and imports are explicit
- As a developer, I want invoke tasks for common operations (lint, format, test, check) so that I can maintain code quality with simple commands

## Specific Requirements

**src Layout Project Structure**
- Use `src/gridfinity_invoke/` as the main package directory
- Distribution name (PyPI): `gridfinity-invoke`
- Import name (Python): `gridfinity_invoke`
- Include `__init__.py` with package version
- Tests directory at project root: `tests/`
- Main `tasks.py` at project root

**pyproject.toml Configuration**
- PEP 517/518 compliant build configuration
- Python 3.11+ requirement
- All tool configurations centralized in pyproject.toml (ruff, pytest, mypy, pyrefly)
- Dependencies: invoke, ruff, pytest, pytest-cov, mypy, pre-commit, colorama, cq-gridfinity, pyrefly, prek
- Entry point for CLI if needed in future

**Ruff Configuration**
- Line length: 88 (black-compatible)
- Rules: E (pycodestyle), F (pyflakes), I (isort)
- Target Python version: 3.11
- Configure in pyproject.toml `[tool.ruff]` section

**Pytest Configuration**
- Configure testpaths to `tests/`
- Enable pytest-cov from day one
- Configure coverage source to `src/gridfinity_invoke`
- Use `[tool.pytest.ini_options]` in pyproject.toml

**Mypy Configuration** (legacy, kept as fallback)
- Strict type checking enabled
- Configure in `[tool.mypy]` section
- Target Python 3.11
- Disallow untyped defs

**Pyrefly Configuration** (primary type checker)
- Meta's Rust-based Python type checker (95% faster than mypy)
- Configure in `[tool.pyrefly]` section
- Set project root and source paths
- Replaces mypy as primary type checker in pre-commit hooks

**Pre-commit Hooks (via prek)**
- Create `.pre-commit-config.yaml`
- Use `prek` instead of `pre-commit` (Rust-based, 7-10x faster)
- Include ruff linting hook
- Include ruff formatting hook
- Include pyrefly type checking hook (replaces mypy)

**Invoke Task: lint**
- Run ruff linter on source and test files
- JSON docstring format for documentation
- Exit with appropriate error code on lint failures

**Invoke Task: format**
- Run ruff formatter on source and test files
- JSON docstring format for documentation
- Support `--check` flag for CI-style validation without modification

**Invoke Task: test**
- Run pytest with coverage reporting
- JSON docstring format for documentation
- Support optional `--verbose` flag
- Display coverage summary

**Invoke Task: check**
- Run lint + test together in sequence
- JSON docstring format for documentation
- Fail fast on lint errors before running tests

**Invoke Task: bin**
- Generate a Gridfinity bin using cq-gridfinity
- Parameters: length, width, height (all in gridfinity units)
- Output STL file to configurable location
- JSON docstring format with param descriptions

**Invoke Task: baseplate**
- Generate a Gridfinity baseplate using cq-gridfinity
- Parameters: length, width (in gridfinity units)
- Output STL file to configurable location
- JSON docstring format with param descriptions

**JSON Docstring Format**
- Format: `""" {"desc": "...", "params": [...], "returns": {}} """`
- Each param object: `{"name": "...", "type": "...", "desc": "...", "example": "..."}`
- Enables structured help output via `invoke --list`
- All tasks must use this format for consistency

**TDD Implementation Approach**
- No dummy implementations or stubs allowed
- Real implementations only
- Tests must pass with actual functionality
- Be critical of code quality
- Ask user for guidance when stuck

## Existing Code to Leverage

**User's invoke library at ~/conx.microservices/tasks.py**
- JSON docstring format pattern for task documentation
- Task aliases pattern: `@task(aliases=['ls'])`
- Collection-based namespace organization
- Colorama usage for colored output
- Format helper function for pretty-printing task help

**Invoke task decorator patterns**
- Use `@task` decorator with optional `aliases` parameter
- Context `ctx` as first parameter for all tasks
- `ctx.run()` for executing shell commands
- Optional parameters with defaults for flexibility

**JSON docstring structure**
- `desc`: Short description of what the task does
- `params`: Array of parameter objects with name, type, desc, example
- `returns`: Object describing return value (usually empty `{}`)
- Boolean params use type `"bool"`, strings use `"string"`, integers use `"int"`

## Out of Scope
- GitHub Actions CI - will never be implemented
- Docker configuration - will never be implemented
- Other infrastructure concerns - will never be implemented
- Complex namespace/collection organization (keep flat for now)
- Custom list command (use standard `invoke --list`)
- Autocomplete generation
- Interactive prompts or user input during tasks
- Project save/load system (future spec)
- GitHub integration tasks (future spec)
