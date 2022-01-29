import os
import shlex
import signal
import subprocess
import sys
from typing import Tuple


def run_system_command(
    command: str, shell: bool = False, timeout_s: int = 30
) -> Tuple[int, str, bool]:
    """run a process, capture the output and wait for it to finish. if timeout is specified then Kill the subprocess and its childrens when the timeout is reached (if parent did not detach)

    Args:
        command (str): command+args. always pass a string, the function will split it when needed.
        shell (bool, optional): shell usage. Defaults to False.
        timeout_s (int): timeout in seconds before force killing. Defaults to 30.

    Returns:
        Tuple[int, str, bool]: exit code, output, and if timeout was reached or not.
    """

    def killAll(ParentPid: int) -> None:
        if sys.platform.startswith("linux"):
            os.killpg(os.getpgid(ParentPid), signal.SIGTERM)
        elif sys.platform.startswith("cygwin"):
            # subprocess.Popen(shlex.split('bash -c "TASKKILL /F /PID $(</proc/{pid}/winpid) /T"'.format(pid=ParentPid)))
            winpid = int(open("/proc/{pid}/winpid".format(pid=ParentPid)).read())
            subprocess.Popen(["TASKKILL", "/F", "/PID", str(winpid), "/T"])
        elif sys.platform.startswith("win32"):
            subprocess.Popen(["TASKKILL", "/F", "/PID", str(ParentPid), "/T"])

    if sys.platform.startswith("darwin"):
        shell = True
    
    # - in windows we never need to split the command, but in cygwin and linux we need to split if shell=False (default), shlex will split the command for us
    if shell == False and (
        sys.platform.startswith("cygwin") or sys.platform.startswith("linux")
    ):
        command = shlex.split(command)

    new_session = False
    if sys.platform.startswith("linux"):
        new_session = True
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=new_session,
        shell=shell,
    )

    try:
        out = p.communicate(timeout=timeout_s)[0].decode("utf-8")
        is_timeout_reached = False
    except subprocess.TimeoutExpired:
        print("Timeout reached: Killing the whole process group...")
        killAll(p.pid)
        out = p.communicate()[0].decode("utf-8")
        is_timeout_reached = True
    return p.returncode, out, is_timeout_reached
