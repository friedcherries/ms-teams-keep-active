#!/usr/bin/env python3
"""
MS Teams Keep Active Script
Multiple methods to prevent Teams from going inactive
"""

import time
import subprocess
import sys
import signal
import random
from datetime import datetime, time as dtime

def exit_after(hour=17, minute=30):
    """
    Function to end program after specific time
    Defaults to 5:30pm
    """
    # Define the cutoff time
    cutoff = dtime(hour, minute)

    # Get the current local time
    now = datetime.now().time()

    # Compare and exit if after cutoff
    if now > cutoff:
        print(f"It is after {hour}:{minute}. Exiting program.")
        sys.exit(0)

class ActivityKeeper:
    """
    Class to simulate variable activity types
    """
    def __init__(self):
        self.methods = [
            self.teams_specific_activity,
            self.mouse_jiggle,
            self.key_combo,
            self.scroll_activity
        ]
        self.current_method = 0

    def mouse_jiggle(self):
        """More noticeable mouse movement"""
        try:
            result = subprocess.run(['xdotool', 'getmouselocation'],
                                  capture_output=True, text=True, check=False)
            if result.returncode != 0:
                return False

            pos_line = result.stdout.strip()
            x = int(pos_line.split()[0].split(':')[1])
            y = int(pos_line.split()[1].split(':')[1])

            # Larger movement pattern
            movements = [(5, 0), (0, 5), (-5, 0), (0, -5)]
            for dx, dy in movements:
                subprocess.run(['xdotool', 'mousemove', str(x+dx), str(y+dy)], check=False)
                time.sleep(0.1)

            # Return to original position
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)], check=False)
            print(f"🖱️  Mouse pattern completed at {time.strftime('%H:%M:%S')}")
            return True
        except Exception as e:
            print(f"❌ Mouse method failed: {e}")
            return False

    def key_combo(self):
        """Send shift key press"""
        try:
            subprocess.run(['xdotool', 'key', 'shift'], check=False)
            time.sleep(0.1)
            print(f"⌨️  Shift key pressed at {time.strftime('%H:%M:%S')}")
            return True
        except Exception as e:
            print(f"❌ Key combo failed: {e}")
            return False

    def scroll_activity(self):
        """Simulate scroll wheel activity"""
        try:
            # Scroll up then down
            subprocess.run(['xdotool', 'click', '4'], check=False)  # Scroll up
            time.sleep(0.2)
            subprocess.run(['xdotool', 'click', '5'], check=False)  # Scroll down
            print(f"🔄 Scroll activity at {time.strftime('%H:%M:%S')}")
            return True
        except Exception as e:
            print(f"❌ Scroll method failed: {e}")
            return False

    def teams_specific_activity(self):
        """Simulate activity specifically within the Teams window"""
        try:
            # Focus the Teams window first
            if not self.focus_teams_window():
                return False

            # Send a very subtle key that Teams might register but won't interfere
            # F15 is usually unbound and safe
            subprocess.run(['xdotool', 'key', 'F15'], check=False)
            time.sleep(0.1)

            # Or try a modifier key
            subprocess.run(['xdotool', 'keydown', 'ctrl'], check=False)
            time.sleep(0.05)
            subprocess.run(['xdotool', 'keyup', 'ctrl'], check=False)

            print(f"📱 Teams-specific activity at {time.strftime('%H:%M:%S')}")
            return True
        except Exception as e:
            print(f"❌ Teams-specific activity failed: {e}")
            return False

    def focus_teams_window(self):
        """Try to focus the Teams Edge app window"""
        try:
            # Look for Edge app windows with Teams-related titles
            search_terms = ['Teams', 'Microsoft Teams', 'teams.microsoft.com']

            for term in search_terms:
                result = subprocess.run(['xdotool', 'search', '--name', '--onlyvisible', term],
                                      capture_output=True, text=True, check=False)
                if result.stdout.strip():
                    window_ids = result.stdout.strip().split('\n')
                    for window_id in window_ids:
                        # Get window info to confirm it's the right one
                        window_info = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                   capture_output=True, text=True, check=False)
                        if 'teams' in window_info.stdout.lower():
                            subprocess.run(['xdotool', 'windowactivate', window_id], check=False)
                            print(f"🎯 Focused Teams window: {window_info.stdout.strip()}")
                            time.sleep(0.3)
                            return True

            # Fallback: look for any Edge process
            result = subprocess.run(['xdotool', 'search', '--class', 'msedge'],
                                  capture_output=True, text=True, check=False)
            if result.stdout.strip():
                window_id = result.stdout.strip().split('\n')[0]  # Get first Edge window
                subprocess.run(['xdotool', 'windowactivate', window_id], check=False)
                print("🌐 Focused Edge window")
                time.sleep(0.3)
                return True

            return False
        except Exception as e:
            print(f"❌ Focus Teams window failed: {e}")
            return False

    def simulate_activity(self):
        """Try multiple methods with rotation, focusing on Teams window"""
        success = False

        # Always try to focus Teams first
        teams_focused = self.focus_teams_window()
        time.sleep(0.5)

        # Try current method
        method = self.methods[self.current_method]
        success = method()

        # If it failed, try the next method
        if not success:
            self.current_method = (self.current_method + 1) % len(self.methods)
            method = self.methods[self.current_method]
            success = method()

        # Rotate method for next time
        self.current_method = (self.current_method + 1) % len(self.methods)

        if teams_focused:
            print("✅ Teams window was focused for activity")
        else:
            print("⚠️  Could not focus Teams window")

        return success

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n🛑 Stopping keeper at {time.strftime('%H:%M:%S')}")
    sys.exit(0)

def main():
    """ Main Entry point """
    # Check dependencies
    try:
        subprocess.run(['which', 'xdotool'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ xdotool not found. Install with: sudo dnf install xdotool")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    keeper = ActivityKeeper()

    # Sleep parameter to be randomly updated with each iteration
    interval_seconds = 0

    print("🚀 MS Teams Keep Active")
    print("🎯 Multiple activity methods, every 2 minutes")
    print("🔄 Rotates between mouse, keyboard, and scroll methods")
    print("⌨️  Press Ctrl+C to stop\n")

    while True:
        exit_after()
        print(f"--- Activity cycle at {time.strftime('%H:%M:%S')} ---")
        keeper.simulate_activity()
        interval_seconds = random.randint(60, 180)
        print(f"⏳ Waiting {interval_seconds//60} minutes...\n")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
