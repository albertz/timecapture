#!/bin/bash

appname="$1"
windowtitle="$2"
[ "$appname" = "" ] && echo "expecting app-name" && exit 1

mydir="$(dirname "$0")"
script="$mydir/app-scripts/url of $appname"

function call_applescript {
	ret="$(osascript -ss "$1" 2>/dev/null)"
	[ $? != 0 ] && return 1
	echo "$ret" | sed "s/^\"\(.*\)\"$/\1/g"
}

[ -e "$script.scpt" ] && {
	call_applescript "$script.scpt"
	exit $?
}

[ -e "$script.sh" ] && {
	sh "$script.sh" "$windowtitle"
	exit $?
}

{
	echo "tell application \"$appname\""
	echo "set weburl to \"file://\" & (path of front document as string)"
	echo "end tell"
} | call_applescript - && exit 0

{
	echo "tell application \"System Events\""
	echo "tell process \"$appname\""
	echo "set weburl to value of attribute \"AXDocument\" of front window"
	echo "end tell"
	echo "end tell"
} | call_applescript - && exit 0

exit 1
