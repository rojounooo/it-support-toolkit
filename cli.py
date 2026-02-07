import subprocess
import pathlib
import json


# Select OS
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

os_choice = int(input("Enter your choice: "))
os_name = os_map.get(os_choice)

if not os_name:
    raise ValueError("Invalid OS selection")


# Select module
modules_path = pathlib.Path("modules")
modules = [m for m in modules_path.iterdir() if m.is_dir()]

print("\nSelect module:")
for i, module in enumerate(modules, start=1):
    print(f"{i}) {module.name}")

module_choice = int(input("Enter your choice: "))
selected_module = modules[module_choice - 1]

# Select tool (from tasks.json)
tasks_file = selected_module / "tasks.json"

if not tasks_file.exists():
    raise FileNotFoundError("tasks.json not found for selected module")

with open(tasks_file, "r") as f:
    tasks = json.load(f)

print("\nSelect tool:")
for i, task in enumerate(tasks, start=1):
    print(f"{i}) {task['name']}")

tool_choice = int(input("Enter your choice: "))
selected_task = tasks[tool_choice - 1]


# Build script path
script_base = selected_task["script"]

if os_name == "windows":
    script_path = selected_module / os_name / f"{script_base}.ps1"
else:
    script_path = selected_module / os_name / f"{script_base}.sh"

# Get parameters
params = selected_task.get("params", [])
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

result = subprocess.run(command, capture_output=True, text=True)

# Final selection summary
print("\nYou selected:")
print(f"OS: {os_name}")
print(f"Module: {selected_module.name}")
print(f"Tool: {selected_task['name']}")
print(f"Script path: {script_path}")
print(f"Parameters: {values}")
print(f"Output: {result.stdout}")