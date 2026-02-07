import os
import platform
import ctypes
import subprocess

def is_admin():
    """Return True if the current user is admin/root, False otherwise."""
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0

def run_command(command, admin_required=False):
    """
    Run a command with optional elevation.
    
    Args:
        command (list): Command as a list of strings.
        admin_required (bool): Whether this command needs admin/root privileges.
    """
    system = platform.system()
    user_is_admin = is_admin()

    if system == "Windows":
        if admin_required and not user_is_admin:
            print("\nThis task requires Administrator privileges. Elevating...")
            # Wrap the command in Start-Process with RunAs
            argument_list = " ".join(command)
            elevated_command = [
                "powershell.exe",
                "-Command",
                f"Start-Process powershell.exe -Verb RunAs -ArgumentList '{argument_list}'"
            ]
            command_to_run = elevated_command
        else:
            command_to_run = command

    else:  # Linux / macOS
        command_to_run = command
        if admin_required and not user_is_admin:
            print("\nThis task requires root privileges. Using sudo...")
            command_to_run.insert(0, "sudo")

    try:
        result = subprocess.run(command_to_run, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None
