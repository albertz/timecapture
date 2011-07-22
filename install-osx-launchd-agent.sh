#!/bin/bash

cd "$(dirname "$0")"
DIR="$(pwd)"
BIN="$DIR/capture.py"

#DIR="$(dirname "$BIN")"

cat >~/Library/LaunchAgents/com.az.TimeCapture.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>TimeCapture</string>
<key>OnDemand</key>
<false/>
<key>Program</key>
<string>$BIN</string>
<key>RunAtLoad</key>
<true/>
<key>WorkingDirectory</key>
<string>$DIR</string>
</dict>
</plist>
EOF
