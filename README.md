# gridfinity-invoke

![Tests](https://github.com/sethdefontenay/gridfinity-invoke/actions/workflows/test.yml/badge.svg)

A CLI tool for generating Gridfinity storage components as STL files. Built on top of [cqgridfinity](https://github.com/michaelgale/cq-gridfinity) and [Invoke](https://www.pyinvoke.org/).

If you've got a drawer full of random stuff and want to organize it with 3D-printed Gridfinity bins, this tool helps you generate the STL files without writing any code.

## What's Gridfinity?

[Gridfinity](https://www.youtube.com/watch?v=ra_9zU-mnl8) is a modular storage system designed by Zack Freedman. Everything is based on a 42mm grid - baseplates snap together, and bins click into place on top. It's become pretty popular in the 3D printing community for organizing workshops, desks, and drawers.

## Quickstart

```bash
curl -O https://raw.githubusercontent.com/sethdefontenay/gridfinity-invoke/master/install.sh
chmod +x install.sh
./install.sh
```

The install script clones the repo, creates a virtual environment, installs dependencies, and verifies everything works.

## Installation

Requires Python 3.11+ and the OpenCASCADE kernel (OCP).

```bash
# Clone the repo
git clone https://github.com/sethdefontenay/gridfinity-invoke.git
cd gridfinity-invoke

# Run the install script
./install.sh
```

Or manually:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Note: `cqgridfinity` depends on CadQuery which needs OCP. If you run into issues, check the [CadQuery installation docs](https://cadquery.readthedocs.io/en/latest/installation.html).

## Running Commands

You need to activate the virtual environment before running invoke commands:

```bash
cd gridfinity-invoke
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

Once activated, you should see `(.venv)` in your terminal prompt. Now you can run invoke commands.

Alternatively, you can run commands without activating by using the full path:

```bash
.venv/bin/invoke gf.baseplate --length=4 --width=4
```

## Quick Start

Generate a 4x4 baseplate:

```bash
invoke gf.baseplate --length=4 --width=4
```

Generate a 2x2x3 bin (2 units wide, 2 units deep, 3 units tall):

```bash
invoke gf.bin --length=2 --width=2 --height=3
```

Files go to `output/` by default.

On first run, you'll be prompted to enter your printer's bed dimensions. This gets saved to `.gf-config` and used for all future commands.

## Commands

Run `invoke --list` to see all commands, or `invoke pp` for prettier output with examples.

### Component Generation

**gf.baseplate** - Generate a baseplate
```bash
invoke gf.baseplate --length=4 --width=4 --output=my-baseplate.stl
```

**gf.bin** - Generate a storage bin
```bash
invoke gf.bin --length=2 --width=2 --height=3 --output=my-bin.stl
```

**gf.drawer-fit** - Generate a baseplate sized for a specific drawer, plus spacers to center it

```bash
invoke gf.drawer-fit --width=500 --depth=400
```

This is handy when you want to fill a drawer. Give it the drawer dimensions in millimeters, and it'll:
- Calculate the largest baseplate that fits (rounding down to whole Gridfinity units)
- Generate spacers to fill the gaps around the edges
- Warn you if the baseplate is too big for your print bed
- Optionally split oversized baseplates into multiple printable pieces

### Project Management

Projects let you save component configurations and regenerate them later.

```bash
# Create a new project
invoke gf.new-project --name=kitchen-drawer

# Generate components (they're automatically saved to the project)
invoke gf.drawer-fit --width=500 --depth=400
invoke gf.bin --length=2 --width=2 --height=3

# List all projects
invoke gf.list-projects

# Regenerate all STLs for a project
invoke gf.load --project=kitchen-drawer
```

Project configs are stored in `projects/<name>/config.json`.

### Configuration

**gf.config** - Manage printer bed configuration

```bash
# Set up printer config interactively
invoke gf.config --init

# Show current config
invoke gf.config --show
```

Config is stored in `.gf-config` and includes your printer's bed dimensions. You'll be prompted to set this up on first use of any gf command.

### Development

```bash
invoke dev.lint      # Run ruff linter
invoke dev.format    # Run ruff formatter
invoke dev.test      # Run pytest with coverage
invoke dev.check     # Run lint + test
```

## Print Bed Configuration

The drawer-fit command checks if generated baseplates will fit on your print bed. On first run, you'll be prompted to enter your bed dimensions, which get saved to `.gf-config`.

To update your config later:

```bash
invoke gf.config --init
```

Defaults are 225x225mm (Elegoo Neptune 4 Pro).

## Project Structure

```
gridfinity-invoke/
├── tasks.py                      # Root invoke file (loads collections)
├── invoke_collections/
│   ├── dev.py                    # Development tasks (lint, format, test)
│   └── gf.py                     # Gridfinity tasks (bin, baseplate, etc.)
├── src/gridfinity_invoke/
│   ├── generators.py             # STL generation functions
│   ├── projects.py               # Project management
│   └── config.py                 # Printer config management
├── tests/                        # Test suite
└── projects/                     # Saved project configs
```

## License

MIT
