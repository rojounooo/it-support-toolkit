import os
import platform
import ctypes
import subprocess
import sys

def is_admin():
    if platform.system() == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
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

    if system == "Windows":
        if not is_admin():

            ps_args = command[1:] + [
                "-NoExit",
                "-Command",
                'Read-Host "Press Enter to exit"'
            ]

            command_to_run = [
                "powershell.exe",
                "-Command",
                "Start-Process",
                "powershell.exe",
                "-Verb", "RunAs",
                "-ArgumentList", ",".join(f'"{arg}"' for arg in ps_args)
            ]

            if dry_run:
                print("\nDry run:")
                print(command_to_run)
                return None

            subprocess.run(command_to_run)
            return None

        else:
            return subprocess.run(
                command,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=True
            )


    if not is_admin():
        command = ["sudo", *command]

    return subprocess.run(
        command,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        text=True
    )


