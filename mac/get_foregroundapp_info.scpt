global frontApp, frontAppName, idleTime, window_name

tell application "System Events"
	set frontApp to first application process whose frontmost is true
end tell

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

return {frontAppName, window_name}
