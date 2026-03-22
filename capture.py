#!/usr/bin/env python3

import better_exchook
import datetime
import time
import os.path
import sys
import argparse
from foreground_app_info import get_app_info

my_dir = os.path.dirname(__file__) or os.getcwd()
user_dir = "~/.TimeCapture"

if sys.platform == "darwin":
    user_dir = "~/Library/Application Support/TimeCapture"
elif sys.platform == "win32":
    from win32com.shell import shellcon, shell

    user_dir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + "/TimeCapture"
else:
    raise Exception(f"missing support for your platform {sys.platform}")

user_dir = os.path.expanduser(user_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sleep", "-s", type=float, default=10, help="sleep interval in seconds")
    parser.add_argument("--no-log", "-n", action="store_true", help="disable writing to log")
    args = parser.parse_args()

    better_exchook.install()

    os.makedirs(user_dir, exist_ok=True)

    while True:
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
