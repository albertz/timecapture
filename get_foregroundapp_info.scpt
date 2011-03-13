tell application "System Events"
	set frontApp to name of first application process whose frontmost is true
end tell

set idleTime to (do shell script "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle,\"\";last}'")

set window_name to ""
tell application frontApp
	if the (count of windows) is not 0 then
		set window_name to name of front window
	end if
end tell

set weburl to ""
if frontApp = "Google Chrome" then
	tell application "Google Chrome"
		if the (count of windows) is not 0 then
			set weburl to URL of first tab of front window
		end if
	end tell
else if frontApp = "Finder" then
	try
		tell application "Finder"
			set weburl to "file://" & POSIX path of ((folder of the front window) as text)
		end tell
	end try
else if frontApp = "Terminal" then
	set p to POSIX path of (path to me) as string
	set weburl to "file://" & (do shell script "sh \"$(dirname \"" & p & "\")/get_foregroundterminal_curdir.sh\"")
else if frontApp = "Xcode" then
	try
		tell application "Xcode"
			set weburl to "file://" & POSIX path of (file of front text document as string)
		end tell
	end try
end if

return {frontApp, window_name, weburl, idleTime}

