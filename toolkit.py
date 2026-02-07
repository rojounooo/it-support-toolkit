import pathlib
import json
from privilege_runner import run_command, run_admin_command

def select_os():
    print("Select OS:")
    print("1) linux")
    print("2) windows")
    print("3) mac")
    os_map = {1: "linux", 2: "windows", 3: "mac"}
    return os_map[int(input("Enter your choice: "))]

def select_module():
    modules_path = pathlib.Path("modules")
    modules = [m for m in modules_path.iterdir() if m.is_dir()]

    print("\nSelect module:")
    for i, module in enumerate(modules, start=1):
        print(f"{i}) {module.name}")

    return modules[int(input("Enter your choice: ")) - 1]

def select_tool(module_path):
    with open(module_path / "tasks.json") as f:
        tasks = json.load(f)

    print("\nSelect tool:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}) {task['name']}")

    return tasks[int(input("Enter your choice: ")) - 1]

def run_script(os_name, module_path, task, dry_run):
    script_base = task["script"]

    if os_name == "windows":
        script_path = module_path / os_name / f"{script_base}.ps1"
        command = [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path.resolve())
        ]
    else:
        script_path = module_path / os_name / f"{script_base}.sh"
        command = ["bash", str(script_path.resolve())]

    params = task.get("params", [])
    if params:
        print("\nEnter parameters:")
        for param in params:
            command.append(input(f"{param}: "))

    runner = run_admin_command if task.get("admin", False) else run_command

    if dry_run:
        runner(command, dry_run=True)
        if input("\nDo you want to actually run this command now? (y/n): ").lower() != "y":
            return
        print("\nExecuting command...")

    runner(command, dry_run=False)

if __name__ == "__main__":
    selected_os = select_os()
    selected_module = select_module()
    selected_tool = select_tool(selected_module)
    dry_run = input("\nRun in dry-run mode? (y/n): ").lower() == "y"
    run_script(selected_os, selected_module, selected_tool, dry_run)
