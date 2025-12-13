# Product Mission

## Pitch

Gridfinity CLI is a Python-based command-line automation tool that helps makers and engineers streamline their Gridfinity 3D printing workflows by providing invoke-powered task management, version-controlled project storage, and easy reproducibility across systems.

## Users

### Primary Customers
- **Solo Makers/Engineers**: Individuals who 3D print Gridfinity organizers for personal workspace optimization
- **Technical Hobbyists**: Users comfortable with CLI tools who want automated, repeatable workflows

### User Personas

**Seth** (30s)
- **Role:** Software Engineer / Maker
- **Context:** Personal workspace organization using 3D-printed Gridfinity components
- **Pain Points:** Forgets custom commands between sessions; manual workflow steps are tedious and error-prone; projects scattered across local files without backup
- **Goals:** Quick access to common Gridfinity generation tasks; version-controlled designs; portable setup that works on any machine

## The Problem

### Workflow Fragmentation
Gridfinity design and generation involves multiple steps: configuring dimensions, generating STL files, organizing projects, and tracking iterations. Without automation, these steps are manual, repetitive, and prone to inconsistency.

**Our Solution:** A unified CLI interface powered by Python's invoke library that wraps Gridfinity generation libraries, providing memorable task commands and consistent workflow execution.

### Lost Configurations
Custom Gridfinity configurations and designs exist only on local machines, making them vulnerable to loss and difficult to reproduce on new systems.

**Our Solution:** GitHub-backed project storage with version control, enabling full project history and easy reinstallation on any system.

### Command Memory Overhead
CLI power users often forget custom commands and flags between sessions, leading to repeated documentation lookups or script archaeology.

**Our Solution:** Invoke's self-documenting task system with `invoke --list` and built-in help, reducing the need to remember complex command syntax.

## Differentiators

### Invoke-Powered Task Management
Unlike raw Python scripts or shell aliases, invoke provides structured task definitions with dependencies, namespaces, and built-in documentation. This results in discoverable, maintainable automation that scales with project complexity.

### Version-Controlled Designs
Unlike local-only Gridfinity tools, every design and configuration is stored in GitHub. This results in full project history, easy sharing, and guaranteed reproducibility.

### Portable by Design
Unlike environment-specific setups, the tool is designed for easy reinstallation with minimal dependencies. This results in consistent workflows across workstations, laptops, or fresh OS installations.

## Key Features

### Core Features
- **Invoke Task Interface:** Run common Gridfinity operations with simple, memorable commands like `invoke generate-bin` or `invoke list-projects`
- **Gridfinity Library Integration:** Leverage Python Gridfinity libraries to generate parametric designs without manual CAD work
- **Project Organization:** Structured project directories with consistent naming and metadata

### Workflow Features
- **GitHub Backup:** Push designs and configurations to GitHub for version control and backup
- **Easy Setup:** Single-command installation and configuration on new systems
- **Task Discovery:** Built-in `invoke --list` shows all available commands with descriptions

### Advanced Features
- **Custom Task Creation:** Extend the tool with personal invoke tasks for specialized workflows
- **Parametric Generation:** Generate Gridfinity components with custom dimensions and configurations
- **Batch Operations:** Process multiple designs or projects in single commands
