#!/usr/bin/env python3

from typing import Optional
import datetime
import time
import os
import os.path
import sys
import ast
import subprocess
import re

mydir = os.path.dirname(__file__) or os.getcwd()
userdir = "~/.TimeCapture"


def local_filename_from_url(filename: str) -> Optional[str]:
    if not filename.startswith("file://"):
        return None
    removestart = lambda s, t: s[len(t) :] if s.startswith(t) else s
    filename = removestart(filename, "file://localhost")
    filename = removestart(filename, "file://")
    return filename


if sys.platform == "darwin":
    userdir = "~/Library/Application Support/TimeCapture"

    def get_app_info():
        try:
            ret = subprocess.Popen(
                ["osascript", "-ss", mydir + "/mac/get_foregroundapp_info.scpt"], stdout=subprocess.PIPE
            ).stdout.read()
            ret = ret.strip().decode("utf-8")
            (ret,) = re.match(r"^{(.*)}$", ret).groups()
            appname, windowtitle = ast.literal_eval("(" + ret + ")")
            idletime = (
                subprocess.Popen(["sh", mydir + "/mac/get_idletime.sh"], stdout=subprocess.PIPE).stdout.read().strip()
            )
            idletime = float(idletime)
            url = (
                subprocess.Popen(["sh", mydir + "/mac/get_app_url.sh", appname, windowtitle], stdout=subprocess.PIPE)
                .stdout.read()
                .strip()
                .decode("utf-8")
            )
            localfn = local_filename_from_url(url)
            if localfn is not None:
                m = re.match(r"(.*/Library/Containers/[^/]*/Data/[^/]*)(.*)", localfn)
                if m and os.path.islink(m.groups()[0]):
                    url = (
                        "file://"
                        + os.path.normpath(os.path.join(os.path.dirname(m.groups()[0]), os.readlink(m.groups()[0])))
                        + m.groups()[1]
                    )
            return {"appName": appname, "windowTitle": windowtitle, "url": url, "idleTime": idletime}
        except Exception as e:
            print(e)
            return None

elif sys.platform == "win32":
    from win32com.shell import shellcon, shell

    userdir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + "/TimeCapture"

    def get_app_info():
        try:
            import win32gui

            # TODO: or maybe win32gui.GetFocus() ?
            hwnd = win32gui.GetForegroundWindow()

            # Request privileges to enable "debug process", so we can
            # later use PROCESS_VM_READ, retardedly required to
            # GetModuleFileNameEx()
            import win32security
            import win32con
            import win32process
            import win32api

            priv_flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
            hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), priv_flags)
            # enable "debug process"
            privilege_id = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
            old_privs = win32security.AdjustTokenPrivileges(
                hToken, 0, [(privilege_id, win32security.SE_PRIVILEGE_ENABLED)]
            )

            # Open the process, and query it's filename
            processid = win32process.GetWindowThreadProcessId(hwnd)
            pshandle = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, processid[1]
            )
            exename = win32process.GetModuleFileNameEx(pshandle, 0)

            # clean up
            win32api.CloseHandle(pshandle)
            win32api.CloseHandle(hToken)

            return {"appName": exename, "windowTitle": win32gui.GetWindowText(hwnd), "url": None, "idleTime": None}

        except Exception as e:
            print(e)
            return None

    print("WARNING: win32 support is untested", file=sys.stderr)

else:
    raise Exception(f"missing support for your platform {sys.platform}")


def main():
    global userdir
    userdir = os.path.expanduser(userdir)
    os.makedirs(userdir, exist_ok=True)

    while True:
        logfile = userdir + "/capture-" + datetime.date.today().isoformat()
        logfile = open(logfile, "a")

        timetuple = datetime.datetime.today().timetuple()[0:6]

        logfile.write(repr((timetuple, get_app_info())) + "\n")
        logfile.close()

        time.sleep(10)


if __name__ == "__main__":
    main()
