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

[ -e "$script.py" ] && {
	python "$script.py" "$windowtitle"
	exit $?
}

# NOTE: This has the huge drawback that it sometimes opens another instance of the app.
# For example, I had several OpenLieroX instances on my PC and has started one of it.
# This little snippet here just started another instance.
# Also, it seems that the fallback below covers anyway all cases.
#{
#	echo "tell application \"$appname\""
#	echo "set weburl to \"file://\" & (path of front document as string)"
#	echo "end tell"
#} | call_applescript - && exit 0

{
	echo "tell application \"System Events\""
	echo "  tell process \"$appname\""
	echo "    tell (1st window whose value of attribute \"AXMain\" is true)"
	echo "      return value of attribute \"AXDocument\""
	echo "    end tell"
	echo "  end tell"
	echo "end tell"
} | call_applescript - && exit 0

exit 1
