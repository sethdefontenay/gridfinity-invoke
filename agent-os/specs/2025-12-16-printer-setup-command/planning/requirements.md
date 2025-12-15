# Spec Requirements: Printer Setup Command & Project Restructure

## Initial Description
The project needs an invoke command for setting up printer size parameters and a few other tidy up tasks.

**Context:** This is for a gridfinity-invoke project - a CLI tool for generating Gridfinity storage components as STL files. It currently has hardcoded print bed constants in generators.py (PRINT_BED_WIDTH_MM = 225, PRINT_BED_DEPTH_MM = 225) that users need to manually edit.

## Requirements Discussion

### First Round Questions

**Q1:** I assume the setup command should persist printer settings to a configuration file (e.g., `~/.gridfinity/config.yaml` or `.gridfinity-config` in the project root) rather than requiring users to re-enter them each session. Is that correct, or should settings only apply to the current session?
**Answer:** Store in `.gf-config` file (leading dot style)

**Q2:** I'm thinking the setup command should be interactive with prompts like "Print bed width [225]: " where the user can press Enter to accept defaults. Should we also support non-interactive mode via CLI flags (e.g., `invoke setup --width=300 --depth=300`) for scripting purposes?
**Answer:** When a user is setting up a project, if `.gf-config` doesn't have printer size values, prompt the user to fill them in and backfill to the config. If values already exist, use them silently and log that you're doing so.

**Q3:** I assume we should validate that print bed dimensions are positive numbers and reasonably sized (e.g., at least 42mm to fit one gridfinity unit, not larger than say 1000mm). Is that correct, or do you have specific validation requirements?
**Answer:** No validation needed - trust the user to enter correct values

**Q4:** The current defaults are for an Elegoo Neptune 4 Pro (225x225mm). Should the setup command offer printer presets (e.g., "Elegoo Neptune 4 Pro", "Prusa MK3S", "Bambu Lab P1S") that auto-fill dimensions, or just accept raw numbers?
**Answer:** No presets - just accept raw width and depth values in mm

**Q5:** You mentioned "a few other tidy up tasks" - could you elaborate on what else should be included in this spec?
**Answer:**
- Restructure invoke tasks into namespaced collections:
  - Create `invoke_collections/` folder
  - `invoke_collections/dev.py` - all development tasks (lint, format, test, check)
  - `invoke_collections/gf.py` - all gridfinity tasks (baseplate, bin, drawer-fit, new-project, load, list-projects)
  - Root `tasks.py` - only pretty print (`pp`) and collection loading
  - Commands should be namespaced: `inv dev.lint`, `inv gf.drawer-fit`, etc.
- Add `install.sh` script for one-click setup that:
  - Clones the project
  - Sets up virtualenv
  - Installs pip packages
  - Runs lint
  - Runs tests

**Q6:** I assume we should add a `invoke config` or `invoke show-config` command to display current settings so users can verify their configuration. Is that correct?
**Answer:** Yes, but under gf namespace: `inv gf.config --init` and `inv gf.config --show`

**Q7:** Is there anything that should explicitly be excluded from this feature (e.g., other printer settings like nozzle size, filament type, etc.)?
**Answer:** Nothing specific excluded

### Existing Code to Reference

**Similar Features Identified:**
- Feature: `prompt_with_default` helper - Path: `/home/seth/tools/gridfinity/tasks.py` (lines 35-49)
- Feature: Active project tracking - Path: `/home/seth/tools/gridfinity/.gridfinity-active` (similar dot-file pattern)
- Feature: Projects module - Path: `/home/seth/tools/gridfinity/src/gridfinity_invoke/projects.py` (file I/O patterns)
- Feature: Print bed constants - Path: `/home/seth/tools/gridfinity/src/gridfinity_invoke/generators.py` (lines 12-18, constants to be replaced with config)

### Follow-up Questions
None required - user provided comprehensive answers.

## Visual Assets

### Files Provided:
No visual assets provided.

### Visual Insights:
N/A

## Requirements Summary

### Functional Requirements

**1. Configuration System (.gf-config)**
- Create `.gf-config` file in project root for persistent settings
- Store printer bed dimensions: width and depth in mm
- Auto-prompt for values when missing during gridfinity operations
- Silently use existing values with log message when present
- No validation required - trust user input

**2. Config Command (`inv gf.config`)**
- `inv gf.config --init`: Interactive prompt to set/update printer dimensions
- `inv gf.config --show`: Display current configuration values
- Prompts should use existing `prompt_with_default` pattern with 225mm defaults

**3. Task Restructure (Namespaced Collections)**
- Create `invoke_collections/` directory
- `invoke_collections/dev.py`: Development tasks
  - `inv dev.lint` - Run ruff linter
  - `inv dev.format` - Run ruff formatter
  - `inv dev.test` - Run pytest
  - `inv dev.check` - Run lint + test sequence
- `invoke_collections/gf.py`: Gridfinity tasks
  - `inv gf.baseplate` - Generate baseplate
  - `inv gf.bin` - Generate bin
  - `inv gf.drawer-fit` - Generate drawer-fit solution
  - `inv gf.new-project` - Create new project
  - `inv gf.load` - Load existing project
  - `inv gf.list-projects` - List all projects
  - `inv gf.config` - Configuration management (--init, --show)
- Root `tasks.py`: Minimal file with:
  - `inv pp` - Pretty print available commands
  - Collection loading/namespace registration

**4. Installation Script (install.sh)**
- One-click setup script for new installations
- Clone the project repository
- Create and activate Python virtualenv
- Install pip packages from pyproject.toml
- Run lint check
- Run test suite
- Provide success/failure feedback

**5. Generator Updates**
- Replace hardcoded `PRINT_BED_WIDTH_MM` and `PRINT_BED_DEPTH_MM` constants
- Read values from `.gf-config` at runtime
- Fallback to defaults (225mm) if config missing
- Trigger config prompt when values needed but missing

### Reusability Opportunities
- `prompt_with_default` function already exists for interactive prompts
- `.gridfinity-active` file pattern can inform `.gf-config` implementation
- Existing `projects.py` has file I/O patterns for config read/write
- JSON docstring format for task help should be maintained

### Scope Boundaries

**In Scope:**
- `.gf-config` file creation and management
- `inv gf.config --init` and `inv gf.config --show` commands
- Restructuring tasks into `invoke_collections/dev.py` and `invoke_collections/gf.py`
- Updating root `tasks.py` to load collections
- Creating `install.sh` script
- Updating generators.py to read from config instead of hardcoded values
- Auto-prompting for config when missing during operations

**Out of Scope:**
- Printer presets or pre-defined printer profiles
- Input validation for printer dimensions
- Other printer settings (nozzle size, filament, etc.)
- Config file location outside project root (e.g., ~/.config/)
- Non-interactive CLI flags for config (only interactive prompts)

### Technical Considerations
- Invoke's namespace/collection system for task organization
- Config file format: likely YAML or JSON (consistent with existing project patterns)
- Shell script compatibility (bash) for install.sh
- Maintain backward compatibility during transition (commands should still work)
- Update `inv pp` to properly display namespaced commands
