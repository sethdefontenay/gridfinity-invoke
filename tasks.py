"""Invoke tasks for gridfinity-invoke project."""

from invoke import Collection, task
from invoke.context import Context
from invoke_collections import dev, gf
from invoke_collections.helpers import format_task_help, print_header


@task
def pp(ctx: Context) -> None:
    """{"desc": "Pretty print all available commands with formatted help", "params": [], "returns": {}}"""  # noqa: E501
    print_header("Available Commands")
    print()

    # Get the namespace
    ns = namespace

    # Collect all tasks from all collections
    all_tasks = []

    # Add root-level tasks
    for task_name, task_obj in ns.tasks.items():
        if not task_name.startswith("_"):
            all_tasks.append((task_name, task_obj.__doc__))

    # Add tasks from sub-collections
    for coll_name, coll in ns.collections.items():
        for task_name, task_obj in coll.tasks.items():
            if not task_name.startswith("_"):
                full_name = f"{coll_name}.{task_name}"
                all_tasks.append((full_name, task_obj.__doc__))

    # Sort and print
    for name, docstring in sorted(all_tasks):
        print(format_task_help(name, docstring))
        print()


# Create the namespace and register collections
namespace = Collection()
namespace.add_collection(dev.dev, name="dev")
namespace.add_collection(gf.gf, name="gf")
namespace.add_task(pp)
