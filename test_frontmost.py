import AppKit
import time
from Foundation import NSRunLoop, NSDate

def _setup():
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    if info:
        info["LSUIElement"] = "1"
    AppKit.NSApplication.sharedApplication().setActivationPolicy_(1)

_setup()

def get_frontmost():
    # Tick run loop
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))
    workspace = AppKit.NSWorkspace.sharedWorkspace()
    front_app = workspace.frontmostApplication()
    active_app = workspace.activeApplication()
    
    front_name = front_app.localizedName() if front_app else "None"
    active_name = active_app.get("NSApplicationName", "None") if active_app else "None"
    
    return f"front: {front_name}, active: {active_name}"

while True:
    print(get_frontmost())
    time.sleep(1)
