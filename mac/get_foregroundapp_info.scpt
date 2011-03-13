tell application "System Events"
	set frontApp to first application process whose frontmost is true
end tell

set idleTime to (do shell script "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle,\"\";last}'")

set window_name to ""
try
	set window_name to name of front window of frontApp
end try

set frontAppName to ""
try
	set frontAppName to name of frontApp
end try

set weburl to ""
try
	if frontAppName = "Google Chrome" then
		tell application "Google Chrome"
			if the (count of windows) is not 0 then
				set weburl to URL of active tab of front window
			end if
		end tell
	else if frontAppName = "Finder" then
		try
			tell application "Finder"
				set weburl to "file://" & POSIX path of ((folder of the front window) as text)
			end tell
		end try
	else if frontAppName = "Terminal" then
		set p to POSIX path of (path to me) as string
		set weburl to "file://" & (do shell script "sh \"$(dirname \"" & p & "\")/get_foregroundterminal_curdir.sh\"")
	else if frontAppName = "Xcode" then
		tell application "Xcode"
			set weburl to "file://" & POSIX path of (file of front text document as string)
		end tell
	end if
end try
if weburl = missing value then
	set weburl to ""
end if

return {frontAppName, window_name, weburl, idleTime}

