#!/usr/bin/python

import capture
from glob import glob
from simpledatecalc import dateAbsDiff, dateVectorize, dateStr, DateVecNorm
import re


info_url_match = re.compile("^http(s?)://[a-z0-9.\-]*facebook.com(/.*)?$")
def match(info):
	return bool(info_url_match.match(info["url"]))

statsday = (0,0,0)
statscount = 0
def update_stats(timestamp, timespan, info):
	global statsday, statscount
	if any(statsday) and timestamp[0:3] != statsday:
		print statsday, ":", dateStr(dateVectorize(statscount))
	if timestamp[0:3] != statsday:
		statsday = timestamp[0:3]
		statscount = 0
	statscount += timespan

last = None
timestamp = (0,) * len(DateVecNorm)
info = None

for fn in glob(capture.userdir + "/capture-????-??-??"):
	for l in open(fn):
		last = (timestamp, info)
		timestamp, info = eval(l)
		#print timestamp, info
		if info is None: continue
		if isinstance(info, tuple): # very old format
			info = dict(zip(("appName", "windowTitle", "url", "idleTime"), info))
		if match(info):
			if last:
				timepassed = dateAbsDiff(timestamp, last[0])
				if timepassed > 20: timepassed = 20
			else:
				timepassed = 10
			if info["idleTime"] > timepassed: continue
			update_stats(timestamp, timepassed, info)
