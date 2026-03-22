#!/usr/bin/env python3

import os
import ast
import re
import argparse
from glob import glob
from typing import Dict, Any, Tuple, Optional
import capture
from simpledatecalc import dateAbsDiff, dateVectorize, dateStr

# Filter for Facebook-related activity
INFO_URL_MATCH = re.compile(r"^http(s?)://[a-z0-9.-]*facebook\.com(/.*)?$")


def matches_filter(info: Dict[str, Any]) -> bool:
    """Check if the captured info matches the tracking filter."""
    url = info.get("url")
    if not url:
        return False
    return bool(INFO_URL_MATCH.match(url))


class StatsTracker:
    def __init__(self):
        self.stats_day = (0, 0, 0)
        self.stats_count = 0

    def flush_day(self):
        """Print current day stats if any exist."""
        if any(self.stats_day):
            print(f"{self.stats_day} : {dateStr(dateVectorize(self.stats_count))}")

    def update(self, timestamp: Tuple[int, ...], timespan: int):
        """Update stats with new activity."""
        day = timestamp[0:3]
        if any(self.stats_day) and day != self.stats_day:
            self.flush_day()
        
        if day != self.stats_day:
            self.stats_day = day
            self.stats_count = 0
            
        self.stats_count += timespan


def process_logs(limit: Optional[int] = None):
    tracker = StatsTracker()
    last_entry: Optional[Tuple[Tuple[int, ...], Dict[str, Any]]] = None
    
    # Process log files in chronological order
    log_files = sorted(glob(os.path.join(capture.userdir, "capture-????-??-??")))
    
    if limit:
        log_files = log_files[-limit:]
    
    for fn in log_files:
        with open(fn, "r") as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith("("):
                    continue
                
                # We expect lines to be (timestamp, info) tuples
                timestamp, info = ast.literal_eval(line)
                    
                if info is None:
                    continue
                    
                # Handle very old tuple format
                if isinstance(info, tuple):
                    info = dict(zip(("appName", "windowTitle", "url", "idleTime"), info))
                
                if matches_filter(info):
                    if last_entry:
                        time_passed = dateAbsDiff(timestamp, last_entry[0])
                        # Cap time gap to avoid issues with suspend/resume
                        if time_passed > 20:
                            time_passed = 20
                    else:
                        time_passed = 10
                        
                    # Ignore if user was idle for longer than the sampling interval
                    # We expect idleTime to be float or int (seconds), or sometimes str in old logs.
                    idle_time = info.get("idleTime", 0)
                    if isinstance(idle_time, str):
                        idle_time = float(idle_time)
                    
                    if not isinstance(idle_time, (int, float)):
                        raise TypeError(f"Unexpected idleTime type in {fn}: {type(idle_time)} ({idle_time!r})")
                            
                    if idle_time > time_passed:
                        continue
                        
                    tracker.update(timestamp, time_passed)
                
                last_entry = (timestamp, info)

    tracker.flush_day()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", "-l", type=int, help="Limit to the last N log files")
    args = parser.parse_args()
    
    process_logs(limit=args.limit)


if __name__ == "__main__":
    main()
