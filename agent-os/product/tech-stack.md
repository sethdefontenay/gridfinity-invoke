# Tech Stack

## Language & Runtime
- **Language:** Python 3.11+
- **Package Manager:** pip with pyproject.toml (PEP 517/518 compliant)
- **Virtual Environment:** venv (standard library)

## Task Management
- **Task Runner:** [invoke](https://www.pyinvoke.org/) - Pythonic task execution library
  - Provides CLI interface with `invoke <task>` or `inv <task>`
  - Self-documenting with `invoke --list` and `invoke <task> --help`
  - Supports task dependencies, namespaces, and configuration

## Gridfinity Generation
- **Primary Library:** [cq-gridfinity](https://github.com/michaelgale/cq-gridfinity) - CadQuery-based Gridfinity generator
  - Pure Python parametric CAD using CadQuery
  - Pre-built Gridfinity components (bins, baseplates, etc.)
  - Customizable dimensions and features
- **STL Output:** Native CadQuery STL export via `exportStl()`

## Code Quality

### Linting & Formatting
- **Linter/Formatter:** [ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter
  - Replaces flake8, isort, and black in a single tool
  - Configured via pyproject.toml

### Type Checking
- **Type Hints:** Python type annotations throughout
- **Type Checker:** [pyrefly](https://github.com/facebook/pyrefly) - Fast Python type checker written in Rust
  - High performance type checking
  - Configured via pyproject.toml

## Testing
- **Test Framework:** [pytest](https://pytest.org/)
  - Fixtures for test setup/teardown
  - Parametrized tests for dimension variations
- **Coverage:** pytest-cov for coverage reporting

## Version Control & Storage
- **VCS:** Git
- **Remote:** GitHub
  - Project storage and backup
  - Version history for designs
  - Potential for GitHub Actions CI (future)

## Project Configuration
- **Project Metadata:** pyproject.toml (single source of truth)
- **Design Configs:** YAML or JSON files for Gridfinity parameters
- **Environment Variables:** python-dotenv for any sensitive configuration (if needed)

## Development Tools
- **Editor Config:** .editorconfig for consistent formatting across editors
- **Pre-commit Hooks:** [pre-commit](https://pre-commit.com/) (optional, for automated linting on commit)

## Directory Structure
```
gridfinity/
├── pyproject.toml          # Project metadata, dependencies, tool config
├── tasks.py                 # Invoke task definitions
├── src/
│   └── gridfinity_invoke/  # Main package
│       ├── __init__.py
│       ├── generator.py    # Gridfinity generation logic
│       ├── projects.py     # Project save/load functionality
│       └── config.py       # Configuration handling
├── tests/
│   └── test_generator.py   # pytest tests
├── projects/                # Generated Gridfinity projects
│   └── <project-name>/
│       ├── config.yaml     # Project parameters
│       └── output/         # Generated STL files
└── agent-os/               # Agent OS configuration
```
