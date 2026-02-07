import os
import platform
import ctypes
import subprocess
import sys

def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0

def run_command(command, admin_required=False, dry_run=False):
    system = platform.system()
    user_is_admin = is_admin()

    if system == "Windows":
        if admin_required and not user_is_admin:
            argument_list = " ".join(command)
            command_to_run = [
                "powershell.exe",
                "-Command",
                f"Start-Process powershell.exe -Verb RunAs -ArgumentList '{argument_list}'"
            ]
        else:
            command_to_run = command
    else:
        command_to_run = command[:]
        if admin_required and not user_is_admin:
            command_to_run.insert(0, "sudo")

    if dry_run:
        print("\nDry run mode: the command that would be executed is:")
        print(" ".join(command_to_run))
        return None

    try:
        return subprocess.run(
            command_to_run,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
    except Exception as e:
        print(f"Failed to execute command: {e}")
        return None
