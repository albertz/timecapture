#!/usr/bin/env python3

import better_exchook
import datetime
import time
import os.path
import sys
from foreground_app_info import get_app_info

mydir = os.path.dirname(__file__) or os.getcwd()
userdir = "~/.TimeCapture"

if sys.platform == "darwin":
    userdir = "~/Library/Application Support/TimeCapture"
elif sys.platform == "win32":
    from win32com.shell import shellcon, shell

    userdir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + "/TimeCapture"
else:
    raise Exception(f"missing support for your platform {sys.platform}")

userdir = os.path.expanduser(userdir)


def main():
    better_exchook.install()

    os.makedirs(userdir, exist_ok=True)

    while True:
        logfile_path = userdir + "/capture-" + datetime.date.today().isoformat()
        timetuple = datetime.datetime.today().timetuple()[0:6]

        try:
            app_info = get_app_info()
            res = (timetuple, app_info)
            res_repr = repr(res)
            with open(logfile_path, "a") as logfile:
                logfile.write(res_repr + "\n")
            print(res_repr)
            sys.stdout.flush()
        except Exception:
            better_exchook.better_exchook(*sys.exc_info(), file=sys.stdout)

        time.sleep(10)


if __name__ == "__main__":
    main()
