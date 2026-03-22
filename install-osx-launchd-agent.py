#!/usr/bin/env python3

"""
Generates and installs a macOS launchd agent plist for TimeCapture.
The agent is configured to run capture.py using the current Python interpreter.
"""

import sys
import textwrap
from pathlib import Path


def install_launchd_agent():
    """
    Creates a launchd plist file in ~/Library/LaunchAgents/ to automatically
    start capture.py on login and keep it running.
    """
    # Only for macOS
    if sys.platform != "darwin":
        print("This script is intended for macOS only.")
        sys.exit(1)

    project_dir = Path(__file__).parent.absolute()
    capture_script = project_dir / "capture.py"
    python_executable = sys.executable
    
    plist_label = "com.az.TimeCapture"
    plist_path = Path.home() / "Library" / "LaunchAgents" / f"{plist_label}.plist"
    
    plist_content = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>{plist_label}</string>
            <key>ProgramArguments</key>
            <array>
                <string>{python_executable}</string>
                <string>{capture_script}</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
            <key>KeepAlive</key>
            <true/>
            <key>WorkingDirectory</key>
            <string>{project_dir}</string>
        </dict>
        </plist>
    """)

    print(f"Writing launchd agent to {plist_path}...")
    plist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(plist_path, "w") as f:
        f.write(plist_content)

    print("\nTo load the agent, run:")
    print(f"  launchctl load {plist_path}")
    print("\nTo unload the agent, run:")
    print(f"  launchctl unload {plist_path}")


if __name__ == "__main__":
    install_launchd_agent()
