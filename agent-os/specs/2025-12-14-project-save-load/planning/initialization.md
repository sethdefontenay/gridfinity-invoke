# Project Save/Load System

## Initial Idea

Implement a project save/load system for the Gridfinity CLI that allows users to:
- Save Gridfinity design configurations to reusable project files
- Load saved configurations to regenerate designs
- List available projects
- Create new projects

## Context from User

Research the existing codebase to understand:
1. Current invoke tasks (bin, baseplate) and their parameters
2. How users might want to save/load configurations
3. What file format makes sense (JSON preferred for simplicity)

Define requirements for:
- Project directory structure (where projects are stored)
- Config file format (what parameters to save)
- Invoke tasks needed (save, load, list-projects, new-project)
- Integration with existing bin/baseplate tasks

Keep it simple - this is a small (S) sized feature. Focus on essential functionality only.
