# gridfinity-invoke

A CLI tool for generating Gridfinity storage components as STL files. Built on top of [cqgridfinity](https://github.com/michaelgale/cq-gridfinity) and [Invoke](https://www.pyinvoke.org/).

If you've got a drawer full of random stuff and want to organize it with 3D-printed Gridfinity bins, this tool helps you generate the STL files without writing any code.

## What's Gridfinity?

[Gridfinity](https://www.youtube.com/watch?v=ra_9zU-mnl8) is a modular storage system designed by Zack Freedman. Everything is based on a 42mm grid - baseplates snap together, and bins click into place on top. It's become pretty popular in the 3D printing community for organizing workshops, desks, and drawers.

## Installation

Requires Python 3.11+ and the OpenCASCADE kernel (OCP).

```bash
# Clone the repo
git clone https://github.com/sethdefontenay/gridfinity-invoke.git
cd gridfinity-invoke

# Create a virtual environment and install dependencies
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
.venv/bin/invoke baseplate --length=4 --width=4
```

## Quick Start

Generate a 4x4 baseplate:

```bash
invoke baseplate --length=4 --width=4
```

Generate a 2x2x3 bin (2 units wide, 2 units deep, 3 units tall):

```bash
invoke bin --length=2 --width=2 --height=3
```

Files go to `output/` by default.

## Commands

Run `invoke --list` to see all commands, or `invoke pp` for prettier output with examples.

### Component Generation

**baseplate** - Generate a baseplate
```bash
invoke baseplate --length=4 --width=4 --output=my-baseplate.stl
```

**bin** - Generate a storage bin
```bash
invoke bin --length=2 --width=2 --height=3 --output=my-bin.stl
```

**drawer-fit** - Generate a baseplate sized for a specific drawer, plus spacers to center it

```bash
invoke drawer-fit --width=500 --depth=400
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
invoke new-project --name=kitchen-drawer

# Generate components (they're automatically saved to the project)
invoke drawer-fit --width=500 --depth=400
invoke bin --length=2 --width=2 --height=3

# List all projects
invoke list-projects

# Regenerate all STLs for a project
invoke load --project=kitchen-drawer
```

Project configs are stored in `projects/<name>/config.json`.

### Development

```bash
invoke lint      # Run ruff linter
invoke format    # Run ruff formatter
invoke test      # Run pytest with coverage
invoke check     # Run lint + test
```

## Print Bed Configuration

The drawer-fit command checks if generated baseplates will fit on your print bed. Defaults are set for an Elegoo Neptune 4 Pro (225x225mm).

To change this, edit the constants at the top of `src/gridfinity_invoke/generators.py`:

```python
PRINT_BED_WIDTH_MM = 225   # Change to your bed width
PRINT_BED_DEPTH_MM = 225   # Change to your bed depth
```

## Project Structure

```
gridfinity-invoke/
├── tasks.py                      # Invoke task definitions
├── src/gridfinity_invoke/
│   ├── generators.py             # STL generation functions
│   └── projects.py               # Project management
├── tests/                        # Test suite
└── projects/                     # Saved project configs
```

## License

MIT
