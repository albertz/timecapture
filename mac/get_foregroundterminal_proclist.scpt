tell application "Terminal"
	do shell script "fuser " & (tty of front tab of front window)
end tell
