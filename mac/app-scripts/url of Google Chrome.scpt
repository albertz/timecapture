tell application "Google Chrome"
	if the (count of windows) is not 0 then
		set weburl to URL of active tab of front window
	end if
end tell

return weburl
