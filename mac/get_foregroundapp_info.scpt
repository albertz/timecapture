global frontApp, frontAppName, windowName

tell application "System Events"
	set frontApp to first application process whose frontmost is true
end tell

set windowName to ""
try
	set windowName to name of front window of frontApp
end try
if windowName = missing value then
	set windowName to ""
end if

set frontAppName to ""
try
	set frontAppName to name of frontApp
end try

return {frontAppName, windowName}
