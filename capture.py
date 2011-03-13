#!/usr/bin/python

import datetime, time
import os, os.path, sys
import ast, subprocess
import re

mydir = os.path.dirname(sys.argv[0])
userdir = "~/.TimeCapture"

if sys.platform == "darwin":
	userdir = "~/Library/Application Support/TimeCapture"
	def get_app_info():
		try:
			ret = subprocess.Popen(["osascript", "-ss", mydir + "/mac/get_foregroundapp_info.scpt"], stdout=subprocess.PIPE).stdout.read()
			ret = ret.strip()
			ret, = re.match("^\{(.*)\}$", ret).groups()
			ret = ast.literal_eval("(" + ret + ")")
			return ret
		except:
			return None
else:
	raise Exception, "missing support for your platform"

userdir = os.path.expanduser(userdir)
try: os.makedirs(userdir)
except: pass

while True:
	logfile = userdir + "/capture-" + datetime.date.today().isoformat()
	logfile = open(logfile, "a")

	timetuple = datetime.datetime.today().timetuple()[0:6]

	logfile.write( repr((timetuple, get_app_info())) + "\n" )
	logfile.close()

	time.sleep(10)
