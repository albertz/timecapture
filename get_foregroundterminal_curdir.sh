#!/bin/bash

function pwdx {
	lsof -a -p $1 -d cwd -n | tail -1 | awk '{print $NF}'
}

for pid in $(osascript "$(dirname "$0")/get_foregroundterminal_proclist.scpt"); do
	pwdx $pid
	break # break on first
done
