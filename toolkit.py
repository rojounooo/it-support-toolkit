import pathlib
import json
from privilege_runner import run_command, is_admin

def select_os():
    print("Select OS:")
    print("1) linux")
    print("2) windows")
    print("3) mac")

    os_map = {1: "linux", 2: "windows", 3: "mac"}

    try:
        os_choice = int(input("Enter your choice: "))
        os_name = os_map.get(os_choice)
        if not os_name:
            raise ValueError("Invalid OS selection")
        return os_name
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")

def select_module():
    modules_path = pathlib.Path("modules")
    if not modules_path.exists():
        raise FileNotFoundError("Modules directory not found")

    modules = [m for m in modules_path.iterdir() if m.is_dir()]
    print("\nSelect module:")
    for i, module in enumerate(modules, start=1):
        print(f"{i}) {module.name}")

    try:
        module_choice = int(input("Enter your choice: "))
        if 1 <= module_choice <= len(modules):
            return modules[module_choice - 1]
        else:
            raise ValueError("Invalid module selection")
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")

def select_tool(module_path):
    tasks_file = module_path / "tasks.json"
    if not tasks_file.exists():
        raise FileNotFoundError("tasks.json not found for selected module")

    with open(tasks_file, "r") as f:
        tasks = json.load(f)

    print("\nSelect tool:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}) {task['name']}")

    try:
        tool_choice = int(input("Enter your choice: "))
        if 1 <= tool_choice <= len(tasks):
            return tasks[tool_choice - 1]
        else:
            raise ValueError("Invalid tool selection")
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")

def run_script(os_name, module_path, task, dry_run=False):
    script_base = task["script"]

    if os_name == "windows":
        script_path = module_path / os_name / f"{script_base}.ps1"
    else:
        script_path = module_path / os_name / f"{script_base}.sh"

    # Get parameters
    params = task.get("params", [])
    values = []

    if params:
        print("\nEnter parameters:")
        for param in params:
            value = input(f"{param}: ")
            values.append(value)

    # Build command
    if os_name == "windows":
        command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path), *values]
    else:
        command = [str(script_path), *values]

    # Run dry-run first if requested
    if dry_run:
        run_command(command, admin_required=task.get("admin", False), dry_run=True)

        # Ask if user wants to actually execute
        execute_input = input("\nDo you want to actually run this command now? (y/n): ").lower().strip()
        if execute_input != "y":
            print("Command skipped.")
            return
        else:
            print("\nExecuting command...")

    # Run the command for real
    result = run_command(command, admin_required=task.get("admin", False), dry_run=False)

    if result:
        print("\nYou selected:")
        print(f"OS: {os_name}")
        print(f"Module: {module_path.name}")
        print(f"Tool: {task['name']}")
        print(f"Script path: {script_path}")
        print(f"Parameters: {values}")
        print("\nOutput:")
        print(result.stdout)
        if result.stderr:
            print("Error Output:")
            print(result.stderr)

if __name__ == "__main__":
    try:
        selected_os = select_os()
        selected_module = select_module()
        selected_tool = select_tool(selected_module)

        # Ask user if they want dry-run mode
        dry_run_input = input("\nRun in dry-run mode? (y/n): ").lower().strip()
        dry_run = dry_run_input == "y"

        run_script(selected_os, selected_module, selected_tool, dry_run=dry_run)
    except Exception as e:
        print(f"Error: {e}")
