tell application "System Events"
	set frontApp to first application process whose frontmost is true
end tell

set idleTime to (do shell script "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle,\"\";last}'")

set window_name to ""
try
	set window_name to name of front window of frontApp
end try
if window_name = missing value then
	set window_name to ""
end if

set frontAppName to ""
try
	set frontAppName to name of frontApp
end try

set weburl to ""
try
	set p to POSIX path of (path to me) as string
	set weburl to (do shell script "sh \"$(dirname \"" & p & "\")/get_app_url.sh\" \"" & frontAppName & "\" \"" & window_name & "\"")
end try
if weburl = missing value then
	set weburl to ""
end if

return {frontAppName, window_name, weburl, idleTime}
