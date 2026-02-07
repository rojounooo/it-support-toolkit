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

def run_command(command, dry_run=False):
    if dry_run:
        print("\nDry run mode: the command that would be executed is:")
        print(" ".join(command))
        return None

    return subprocess.run(
        command,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True
    )

def run_admin_command(command, dry_run=False):
    system = platform.system()
    user_is_admin = is_admin()

    if system == "Windows":
        if not user_is_admin:
            argument_list = " ".join(command)
            command_to_run = [
                "powershell.exe",
                "-Command",
                f"Start-Process powershell.exe -Verb RunAs -ArgumentList '{argument_list}'"
            ]
        else:
            command_to_run = command
    else:
        if not user_is_admin:
            command_to_run = ["sudo", *command]
        else:
            command_to_run = command

    if dry_run:
        print("\nDry run mode: the command that would be executed is:")
        print(" ".join(command_to_run))
        return None

    return subprocess.run(
        command_to_run,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True
    )
