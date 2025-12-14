# Specification: Project Save/Load System

## Goal
Enable users to organize Gridfinity designs into named projects with persistent configuration and automatic STL output management.

## User Stories
- As a user, I want to create named projects so that I can organize related Gridfinity components together
- As a user, I want bin/baseplate tasks to automatically save to my active project so that I don't have to specify output paths manually

## Specific Requirements

**Project Directory Structure**
- All projects stored under `projects/<project-name>/` relative to repository root
- Each project contains a `config.json` file and generated STL files
- STL files named after component names (e.g., `main-bin.stl`, `base.stl`)
- Create `projects/` directory automatically if it doesn't exist

**Config File Format**
- JSON format stored as `config.json` in each project directory
- Required fields: `name` (string), `components` (array)
- Component objects contain: `name`, `type` ("bin" or "baseplate"), and dimension parameters
- Bin components: `length`, `width`, `height` (all integers)
- Baseplate components: `length`, `width` (integers)

**Active Project State**
- Track active project in `.gridfinity-active` file at repository root
- File contains single line with project name (no JSON wrapper needed)
- `new-project` task sets newly created project as active
- `load` task sets loaded project as active
- If no active project, bin/baseplate tasks use default `output/` directory behavior

**Invoke Task: new-project**
- Signature: `invoke new-project --name=<name>`
- Creates `projects/<name>/` directory with empty `config.json`
- Initial config: `{"name": "<name>", "components": []}`
- Sets the new project as active (writes to `.gridfinity-active`)
- Fails with error if project already exists

**Invoke Task: load**
- Signature: `invoke load --project=<name>`
- Reads `projects/<name>/config.json`
- Regenerates all STL files for each component in config
- Sets loaded project as active
- Fails with error if project doesn't exist

**Invoke Task: list-projects**
- Signature: `invoke list-projects`
- Lists all directories under `projects/`
- Marks the active project with an asterisk or similar indicator
- Shows "No projects found" if `projects/` is empty or doesn't exist

**Modified bin Task**
- When active project exists: suggest default name like `bin-2x2x3` based on dimensions
- Prompt user to confirm or enter custom name (e.g., "Name [bin-2x2x3]: ")
- Save STL to `projects/<active>/` with the component name
- Add component entry to `config.json` (avoid duplicates by name)
- When no active project: use existing behavior (save to `output/bin.stl`)

**Modified baseplate Task**
- When active project exists: suggest default name like `baseplate-4x4` based on dimensions
- Prompt user to confirm or enter custom name
- Save STL to `projects/<active>/` with the component name
- Add component entry to `config.json` (avoid duplicates by name)
- When no active project: use existing behavior (save to `output/baseplate.stl`)

## Existing Code to Leverage

**tasks.py - Existing invoke task patterns**
- JSON docstring format for task documentation (desc, params, returns)
- `print_header()`, `print_success()`, `print_error()` helper functions for consistent output
- Colorama usage for colored terminal output
- `ctx.run()` pattern for shell commands
- Parameter validation pattern with early exit on error

**generators.py - STL generation functions**
- `generate_bin(length, width, height, output_path)` - generates bin STL
- `generate_baseplate(length, width, output_path)` - generates baseplate STL
- Both functions handle directory creation via `Path.parent.mkdir(parents=True, exist_ok=True)`
- Return Path object of generated file

**Path handling patterns**
- Use `pathlib.Path` for all file operations
- `output_path.parent.mkdir(parents=True, exist_ok=True)` for directory creation
- String conversion with `str(path)` when needed for external libraries

## Out of Scope
- Config validation or JSON schema enforcement
- Project templates or presets
- Project deletion task
- Project rename task
- Component removal from projects
- Version tracking or history
- Project export/import (zip archives)
- Remote project storage or sync
- GUI or web interface
- Undo/redo functionality
