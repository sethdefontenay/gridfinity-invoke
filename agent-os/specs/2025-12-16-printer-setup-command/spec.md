# Specification: Printer Setup Command & Project Restructure

## Goal
Create a configuration system for printer bed dimensions, restructure invoke tasks into namespaced collections, and add an installation script for one-click project setup.

## User Stories
- As a user, I want to configure my printer's bed dimensions once so that generated components fit my printer without manual code edits.
- As a user, I want organized namespaced commands so that I can easily find and run development vs gridfinity tasks.

## Specific Requirements

**Configuration File (.gf-config)**
- Create `.gf-config` file in project root using JSON format (consistent with existing config.json pattern)
- Store `print_bed_width_mm` and `print_bed_depth_mm` values
- File created automatically when printer dimensions first needed
- Use 225mm as default for both width and depth (Elegoo Neptune 4 Pro)

**Config Command (inv gf.config)**
- `--init` flag: Interactive prompts to set/update printer dimensions using `prompt_with_default` pattern
- `--show` flag: Display current configuration values with formatted output
- At least one flag required; show error with usage hint if neither provided
- Log message when using existing config values silently during operations

**Auto-prompt for Missing Config**
- When gridfinity commands need printer dimensions and `.gf-config` is missing or incomplete, prompt user interactively
- Backfill prompted values to `.gf-config` file after user input
- Log message confirming config was saved

**Generator Module Updates**
- Remove hardcoded `PRINT_BED_WIDTH_MM` and `PRINT_BED_DEPTH_MM` constants from generators.py
- Add function to read printer config from `.gf-config` file
- Keep `GRIDFINITY_UNIT_MM` and `MIN_SPACER_GAP_MM` as constants (not configurable)
- Recalculate `MAX_GRIDFINITY_UNITS_X/Y` dynamically from config values

**Task Restructure - invoke_collections/dev.py**
- Create `invoke_collections/` directory
- Move development tasks: `lint`, `format`, `test`, `check`
- Commands become: `inv dev.lint`, `inv dev.format`, `inv dev.test`, `inv dev.check`
- Maintain existing JSON docstring format for help text

**Task Restructure - invoke_collections/gf.py**
- Move gridfinity tasks: `baseplate`, `bin`, `drawer-fit`, `new-project`, `load`, `list-projects`
- Add new `config` task with `--init` and `--show` flags
- Commands become: `inv gf.baseplate`, `inv gf.bin`, etc.
- Import config reading functions from projects.py or new config module

**Root tasks.py Minimal File**
- Keep only `pp` (pretty print) command at root level
- Import and register `dev` and `gf` collections as namespaces
- Update `pp` to properly enumerate and display namespaced commands

**Installation Script (install.sh)**
- Bash script in project root for one-click setup
- Clone project (or assume already cloned if running from repo)
- Create Python virtualenv (python -m venv .venv)
- Activate virtualenv and install dependencies from pyproject.toml (pip install -e .)
- Run lint check (inv dev.lint)
- Run test suite (inv dev.test)
- Print success/failure summary with next steps

## Visual Design
No visual assets provided.

## Existing Code to Leverage

**prompt_with_default function (tasks.py lines 35-49)**
- Displays prompt as "Name [default]: " format
- Returns user input or default if empty
- Reuse directly for printer dimension prompts in config command

**Active file pattern (projects.py lines 11, 14-23)**
- `.gridfinity-active` uses simple text file for state
- `get_active_project()` shows read pattern with try/except FileNotFoundError
- Apply similar pattern for `.gf-config` but use JSON for structured data

**Project config I/O (projects.py lines 47-75)**
- `load_project_config()` and `save_project_config()` use JSON with indent=2
- Path handling with `mkdir(parents=True, exist_ok=True)`
- Follow same JSON formatting and error handling patterns

**Print helpers (tasks.py lines 15-32)**
- `print_header()`, `print_success()`, `print_error()`, `print_warning()` for consistent CLI output
- Move to shared location or import from tasks.py into collections

**JSON docstring format for task help**
- Tasks use JSON in docstrings: `{"desc": "...", "params": [...], "returns": {}}`
- `format_task_help()` parses and pretty prints these
- Maintain this format for all tasks in new collection files

## Out of Scope
- Printer presets or pre-defined printer profiles
- Input validation for printer dimensions (trust user input)
- Other printer settings (nozzle size, filament type, layer height)
- Config file location outside project root (no ~/.config/ support)
- Non-interactive CLI flags for setting config values directly
- Migration of existing project configs
- Windows batch file equivalent of install.sh
- Backward compatibility shims for old command names (inv lint vs inv dev.lint)
- Printer bed shape configurations (only rectangular supported)
- Multi-printer profile support
