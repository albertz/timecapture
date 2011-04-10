#!/bin/bash

function pwdx {
	lsof -a -p $1 -d cwd -n -Fn | grep -E "^n" | sed "s/^n//"
}

for pid in $(osascript "$(dirname "$0")/get_foregroundterminal_proclist.scpt"); do
	pwdx $pid
	break # break on first
done
