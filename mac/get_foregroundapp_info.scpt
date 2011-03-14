global frontApp, frontAppName, windowName

set windowName to ""
tell application "System Events"
	set frontApp to first application process whose frontmost is true
	try
		set windowName to (name of front window of frontApp) as string
	end try
end tell
if windowName = missing value then
	set windowName to ""
end if

set frontAppName to ""
try
	set frontAppName to name of frontApp
end try

return {frontAppName, windowName}
