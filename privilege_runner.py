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

def run_command(command, admin_required=False, dry_run=False):
    """
    Run a command with optional elevation or just preview it in dry-run mode.

    Args:
        command (list): Command as a list of strings.
        admin_required (bool): Whether this command needs admin/root privileges.
        dry_run (bool): If True, only prints the command without executing.
    """
    system = platform.system()
    user_is_admin = is_admin()

    if system == "Windows":
        if admin_required and not user_is_admin:
            # Elevate using Start-Process with RunAs
            argument_list = " ".join(command)
            command_to_run = [
                "powershell.exe",
                "-Command",
                f"Start-Process powershell.exe -Verb RunAs -ArgumentList '{argument_list}'"
            ]
        else:
            command_to_run = command
    else:  # Linux / macOS
        command_to_run = command
        if admin_required and not user_is_admin:
            command_to_run.insert(0, "sudo")

    if dry_run:
        print("\nDry run mode: the command that WOULD be executed is:")
        print(" ".join(command_to_run))
        return None

    try:
        result = subprocess.run(command_to_run, capture_output=True, text=True)
        return result
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None
