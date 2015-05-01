#!/usr/bin/python

import better_exchook
better_exchook.install()

import datetime, time
import os, os.path, sys
import ast, subprocess
import re
from foreground_app_info import get_app_info

mydir = os.path.dirname(__file__) or os.getcwd()
userdir = "~/.TimeCapture"

if sys.platform == "darwin":
	userdir = "~/Library/Application Support/TimeCapture"
elif sys.platform == "win32":
	from win32com.shell import shellcon, shell
	userdir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) + "/TimeCapture"
else:
	raise Exception, "missing support for your platform"

userdir = os.path.expanduser(userdir)
try: os.makedirs(userdir)
except Exception: pass

def main():
	while True:
		logfile = userdir + "/capture-" + datetime.date.today().isoformat()
		logfile = open(logfile, "a")

		timetuple = datetime.datetime.today().timetuple()[0:6]

		logfile.write( repr((timetuple, get_app_info())) + "\n" )
		logfile.close()

		time.sleep(10)

if __name__ == "__main__":
	main()
