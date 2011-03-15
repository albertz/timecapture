#!/usr/bin/python

import datetime, time
import os, os.path, sys
import ast, subprocess
import re

mydir = os.path.dirname(sys.argv[0]) or os.getcwd()
userdir = "~/.TimeCapture"

if sys.platform == "darwin":
	userdir = "~/Library/Application Support/TimeCapture"
	def get_app_info():
		try:
			ret = subprocess.Popen(["osascript", "-ss", mydir + "/mac/get_foregroundapp_info.scpt"], stdout=subprocess.PIPE).stdout.read()
			ret = ret.strip()
			ret, = re.match("^\{(.*)\}$", ret).groups()
			appname,windowtitle = ast.literal_eval("(" + ret + ")")
			idletime = subprocess.Popen(["sh", mydir + "/mac/get_idletime.sh"], stdout=subprocess.PIPE).stdout.read().strip()
			idletime = float(idletime)
			url = subprocess.Popen(["sh", mydir + "/mac/get_app_url.sh", appname, windowtitle], stdout=subprocess.PIPE).stdout.read().strip()
			return {"appName":appname, "windowTitle":windowtitle, "url":url, "idleTime":idletime}
		except Exception, e:
			print e
			return None
else:
	raise Exception, "missing support for your platform"

def main():
	global userdir
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

if __name__ == "__main__":
	main()
