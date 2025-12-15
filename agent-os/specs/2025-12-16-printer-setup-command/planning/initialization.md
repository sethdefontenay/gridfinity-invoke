# Spec Initialization

## Raw Idea
The project needs an invoke command for setting up printer size parameters and a few other tidy up tasks.

## Context
This is for a gridfinity-invoke project - a CLI tool for generating Gridfinity storage components as STL files. It currently has hardcoded print bed constants in generators.py (PRINT_BED_WIDTH_MM = 225, PRINT_BED_DEPTH_MM = 225) that users need to manually edit.
