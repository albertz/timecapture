#!/usr/bin/python

import datetime, time
import os, os.path, sys
import ast, subprocess
import re

mydir = os.path.dirname(sys.argv[0])

if sys.platform == "darwin":
	def get_app_info():
		ret = subprocess.Popen(["osascript", "-ss", mydir + "/get_foregroundapp_info.scpt"], stdout=subprocess.PIPE).stdout.read()
		ret = ret.strip()
		ret, = re.match("^\{(.*)\}$", ret).groups()
		ret = ast.literal_eval("(" + ret + ")")
		return ret
else:
	raise Exception, "missing support for your platform"

try: os.mkdir(os.path.expanduser("~/.timecapture"))
except: pass

while True:
	logfile = "~/.timecapture/capture-" + datetime.date.today().isoformat()
	logfile = os.path.expanduser(logfile)

	logfile = open(logfile, "a")

	timetuple = datetime.datetime.today().timetuple()[0:6]

	logfile.write( repr((timetuple, get_app_info())) + "\n" )
	logfile.close()

	time.sleep(10)
