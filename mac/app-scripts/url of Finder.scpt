tell application "Finder"
	set weburl to "file://" & POSIX path of ((folder of the front window) as text)
end tell

return weburl
