#!/bin/bash

appname="$1"
windowtitle="$2"
[ "$appname" = "" ] && echo "expecting app-name" && exit 1

mydir="$(dirname "$0")"
script="$mydir/app-scripts/url of $appname"

[ -e "$script.scpt" ] && {
	osascript -ss "$script.scpt" 2>/dev/null | sed "s/^\"\(.*\)\"$/\1/g"
	exit $?
}

[ -e "$script.sh" ] && {
	sh "$script.sh" "$windowtitle"
	exit $?
}

exit 1
