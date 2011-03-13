tell application "Xcode"
	set weburl to "file://" & POSIX path of (file of front text document as string)
end tell

return weburl
