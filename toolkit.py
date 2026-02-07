import pathlib
import json
from privilege_runner import run_command

def select_os():
    print("Select OS:")
    print("1) linux")
    print("2) windows")
    print("3) mac")

    os_map = {1: "linux", 2: "windows", 3: "mac"}
    os_choice = int(input("Enter your choice: "))
    return os_map[os_choice]

def select_module():
    modules_path = pathlib.Path("modules")
    modules = [m for m in modules_path.iterdir() if m.is_dir()]

    print("\nSelect module:")
    for i, module in enumerate(modules, start=1):
        print(f"{i}) {module.name}")

    module_choice = int(input("Enter your choice: "))
    return modules[module_choice - 1]

def select_tool(module_path):
    tasks_file = module_path / "tasks.json"
    with open(tasks_file) as f:
        tasks = json.load(f)

    print("\nSelect tool:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}) {task['name']}")

    tool_choice = int(input("Enter your choice: "))
    return tasks[tool_choice - 1]

def run_script(os_name, module_path, task, dry_run):
    script_base = task["script"]

    if os_name == "windows":
        script_path = module_path / os_name / f"{script_base}.ps1"
    else:
        script_path = module_path / os_name / f"{script_base}.sh"

    abs_script_path = str(script_path.resolve())

    params = task.get("params", [])
    values = []

    if params:
        print("\nEnter parameters:")
        for param in params:
            values.append(input(f"{param}: "))

    if os_name == "windows":
        command = [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            abs_script_path,
            *values
        ]
    else:
        command = ["bash", abs_script_path, *values]

    if dry_run:
        run_command(
            command,
            admin_required=task.get("admin", False),
            dry_run=True
        )

        execute = input("\nDo you want to actually run this command now? (y/n): ").lower()
        if execute != "y":
            return

        print("\nExecuting command...")

    run_command(
        command,
        admin_required=task.get("admin", False),
        dry_run=False
    )

if __name__ == "__main__":
    selected_os = select_os()
    selected_module = select_module()
    selected_tool = select_tool(selected_module)
    dry_run = input("\nRun in dry-run mode? (y/n): ").lower() == "y"
    run_script(selected_os, selected_module, selected_tool, dry_run)
