# Project Structure Setup - Requirements

## Decisions Made

### 1. Project Layout
- **Decision**: src layout (`src/gridfinity_invoke/`)
- **Rationale**: Easier to test - forces proper installation, prevents accidental local imports, cleaner test isolation

### 2. Starter Invoke Tasks
- `lint` - run ruff linter
- `format` - run ruff formatter
- `test` - run pytest
- `check` - runs lint + test together
- `bin` - generate a gridfinity bin (params: height, width, length in gridfinity units)
- `baseplate` - generate a gridfinity baseplate (params: height, width in gridfinity units)

### 3. Ruff Configuration
- **Decision**: Use ruff's recommended/popular defaults
- Rules: E (pycodestyle), F (pyflakes), I (isort), plus common best practices
- Line length: 88 (black-compatible)

### 4. Pytest Setup
- **Decision**: Include pytest-cov from day one
- Coverage reporting enabled immediately

### 5. Package Naming
- **Distribution name (PyPI)**: `gridfinity-invoke`
- **Import name (Python)**: `gridfinity_invoke`

### 6. Implementation Approach
- **Decision**: TDD style - NO dummy implementations or stubs
- Real implementations only
- Tests must pass with actual functionality
- Ask user for advice when stuck (user is senior engineer with decades of experience)
- Never report tests as passing with simplified/temporary solutions
- Always be critical of the code

### 7. Optional Tooling
- **Decision**: Include modern Rust-based tooling for performance
- prek (Rust-based pre-commit replacement, 7-10x faster)
- pyrefly (Meta's Rust-based type checker, 95% faster than mypy)
- Keep mypy and pre-commit as fallback options

### 8. Out of Scope (Permanently)
- GitHub Actions CI - will never be implemented
- Docker configuration - will never be implemented
- Other infrastructure concerns - will never be implemented

### 9. Gridfinity Library
- **Decision**: Use cq-gridfinity as the base Python library
- CadQuery-based gridfinity generator

### 10. Docstring Style
- **Decision**: Use JSON-formatted docstrings (matching user's existing invoke library)
- Format: `""" {"desc": "...", "params": [...], "returns": {}} """`
- Provides comprehensive CLI documentation via `invoke --list`

## Reference Code
- User's extensive invoke library at `~/conx.microservices/invoketasks/`
- Key patterns to follow:
  - JSON docstrings for structured help
  - Task aliases (`@task(aliases=['ls'])`)
  - Collection-based namespace organization
  - Colorama for colored output
  - Tasks organized into separate modules

## Visual Assets
- None provided
