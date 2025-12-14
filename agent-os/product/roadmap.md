# Product Roadmap

1. [ ] Project Structure Setup — Establish Python project layout with pyproject.toml, src directory structure, and invoke tasks.py foundation `S`
2. [ ] Gridfinity Library Integration — Research and integrate a Python Gridfinity library (e.g., gridfinity-rebuilt or similar) with basic generation capability exposed via invoke task `M`
3. [ ] Basic Bin Generation Task — Create invoke task to generate standard Gridfinity bins with configurable grid units (width x depth x height) and output STL files `S`
4. [x] Project Save/Load System — Implement project directory structure with JSON/YAML config files to save and reload Gridfinity design parameters `S`
5. [ ] GitHub Integration — Add invoke tasks to initialize git repo, commit changes, and push projects to GitHub with meaningful commit messages `S`
6. [ ] Baseplate Generation Task — Add invoke task to generate Gridfinity baseplates with configurable grid dimensions `S`
7. [ ] Custom Task Template — Create a template/example for adding custom invoke tasks, with documentation on extending the tool `XS`
8. [ ] Setup/Install Script — Create invoke task or shell script for easy installation on new systems (dependencies, git clone, virtual environment) `S`
9. [ ] Batch Generation — Add capability to generate multiple components from a single config file or command `M`
10. [ ] Divider/Insert Generation — Add invoke tasks for generating bin dividers, label holders, or other Gridfinity accessories `M`
11. [ ] Configuration Profiles — Support named configuration profiles for frequently used bin sizes or project templates `S`
12. [ ] Export Manifest — Generate a manifest file listing all STL files in a project with their parameters for easy reference `XS`
13. [x] Smart Baseplate Sizing — Allow users to provide physical dimensions (width and length in mm) of a space they want to fill; the tool calculates how many gridfinity units fit (1 unit = 42mm) and generates an appropriately sized baseplate `S`
14. [ ] Baseplate Tabs Research — Investigate cqgridfinity API for adding mounting tabs around baseplate edges; document available options and implement if supported `XS`

> Notes
> - Order reflects technical dependencies: project structure first, then library integration, then features that build on that foundation
> - Each item represents a complete, testable feature that adds value independently
> - GitHub integration prioritized early to establish backup workflow from the start
> - Batch and advanced features deferred until core single-item workflow is solid
> - Smart Baseplate Sizing (item 13) extends baseplate generation with dimension-to-units conversion
> - Baseplate Tabs (item 14) is a research/exploration item dependent on cqgridfinity capabilities
