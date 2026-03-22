#!/usr/bin/env python3

import better_exchook
import datetime
import time
import os
import sys
import argparse
import importlib
from foreground_app_info import get_app_info


def get_user_dir() -> str:
    """Returns the platform-specific directory for storing TimeCapture data."""
    if sys.platform == "darwin":
        path = "~/Library/Application Support/TimeCapture"
    elif sys.platform == "win32":
        from win32com.shell import shellcon, shell
        path = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + "/TimeCapture"
    else:
        raise Exception(f"missing support for your platform {sys.platform}")
    return os.path.expanduser(path)


def get_latest_mtime(path: str) -> float:
    """Recursively find the latest modification time of any .py file."""
    max_mtime = 0.0
    for root, _, files in os.walk(path):
        if "__pycache__" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                mtime = os.path.getmtime(os.path.join(root, file))
                if mtime > max_mtime:
                    max_mtime = mtime
    return max_mtime


def reload_modules():
    """Reload all loaded submodules of foreground_app_info."""
    print("Reloading modules...")
    
    # Identify all loaded modules that are part of the foreground_app_info package
    prefix = "foreground_app_info"
    submodules = [
        name for name in sys.modules
        if name == prefix or name.startswith(prefix + ".")
    ]
    
    # Sort by length descending to reload submodules before parent modules
    # (though in many cases the exact order doesn't matter for pure logic modules)
    submodules.sort(key=len, reverse=True)
    
    for name in submodules:
        importlib.reload(sys.modules[name])
    
    # Update the global get_app_info reference
    global get_app_info
    from foreground_app_info import get_app_info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", "-s", type=float, default=10, help="sleep interval in seconds")
    parser.add_argument("--no-log", "-n", action="store_true", help="disable writing to log")
    parser.add_argument("--hot-reload", action="store_true", help="enable hot reloading of modules")
    args = parser.parse_args()

    better_exchook.install()

    user_dir = get_user_dir()
    os.makedirs(user_dir, exist_ok=True)
    
    my_dir = os.path.dirname(__file__) or os.getcwd()
    last_mtime = get_latest_mtime(my_dir) if args.hot_reload else 0

    while True:
        if args.hot_reload:
            current_mtime = get_latest_mtime(my_dir)
            if current_mtime > last_mtime:
                reload_modules()
                last_mtime = current_mtime

        logfile_path = user_dir + "/capture-" + datetime.date.today().isoformat()
        timetuple = datetime.datetime.today().timetuple()[0:6]

        try:
            app_info = get_app_info()
            res = (timetuple, app_info)
            res_repr = repr(res)
            if not args.no_log:
                with open(logfile_path, "a") as logfile:
                    logfile.write(res_repr + "\n")
            print(res_repr)
            sys.stdout.flush()
        except Exception:
            better_exchook.better_exchook(*sys.exc_info(), file=sys.stdout)

        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
