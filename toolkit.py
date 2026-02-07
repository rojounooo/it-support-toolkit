import subprocess
import pathlib
import json


def select_os():
    """Prompts the user to select an operating system."""
    print("Select OS:")
    print("1) linux")
    print("2) windows")
    print("3) mac")

    # Map OS choices to OS names, dictionary allows for future expansion
    os_map = {
        1: "linux",
        2: "windows",
        3: "mac"
    }

    try:
        os_choice = int(input("Enter your choice: "))
        os_name = os_map.get(os_choice)

        if not os_name:
            raise ValueError("Invalid OS selection")
        
        return os_name
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")


def select_module():
    """Prompts the user to select a module from the 'modules' directory."""
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
    """Prompts the user to select a tool from the module's tasks.json."""
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


def run_script(os_name, module_path, task):
    """Constructs the script path, gets parameters, and runs the script."""
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

    # Run script
    if os_name == "windows":
        command = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path), *values]
    else:
        command = [str(script_path), *values]

    try:
        result = subprocess.run(command, capture_output=True, text=True)

        # Final selection summary
        print("\nYou selected:")
        print(f"OS: {os_name}")
        print(f"Module: {module_path.name}")
        print(f"Tool: {task['name']}")
        print(f"Script path: {script_path}")
        print(f"Parameters: {values}")
        print(f"Output: {result.stdout}")
        
        if result.stderr:
            print(f"Error Output: {result.stderr}")

    except Exception as e:
        print(f"Failed to execute script: {e}")


if __name__ == "__main__":
    try:
        selected_os = select_os()
        selected_module = select_module()
        selected_tool = select_tool(selected_module)
        run_script(selected_os, selected_module, selected_tool)
    except Exception as e:
        print(f"Error: {e}")
