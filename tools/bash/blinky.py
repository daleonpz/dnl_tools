#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys
from pathlib import Path

PID_FILE = "/tmp/blinky.pid"

def get_current_brightness():
    """Get current screen brightness using xrandr."""
    try:
        output = subprocess.check_output(["xrandr", "--current", "--verbose"]).decode()
        for line in output.splitlines():
            if "Brightness" in line:
                return float(line.split(":")[1].strip())
        return 1.0
    except subprocess.CalledProcessError:
        return 1.0

def set_brightness(value):
    """Set screen brightness using xrandr."""
    try:
        # Get primary display
        output = subprocess.check_output(["xrandr", "--current"]).decode()
        for line in output.splitlines():
            if " connected" in line:
                display = line.split()[0]
                subprocess.run(["xrandr", "--output", display, "--brightness", str(value)])
                break
    except subprocess.CalledProcessError:
        pass

def blink_screen():
    """Blink screen 2 times by adjusting brightness."""
    original_brightness = get_current_brightness()
    for _ in range(2):
        set_brightness(original_brightness * 0.5)  # Dim to 50%
        time.sleep(0.1)
        set_brightness(original_brightness)  # Restore
        time.sleep(0.1)

def start_blinking():
    """Start the blinking daemon."""
    if os.path.exists(PID_FILE):
        print("Blinky is already running.")
        sys.exit(1)

    # Fork to run in background
    pid = os.fork()
    if pid > 0:
        # Parent process exits
        print("Blinky started.")
        sys.exit(0)

    # Child process continues
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    try:
        while True:
            blink_screen()
            time.sleep(60)  # Wait 1 minute
    except KeyboardInterrupt:
        pass
    finally:
        os.remove(PID_FILE)

def stop_blinking():
    """Stop the blinking daemon."""
    if not os.path.exists(PID_FILE):
        print("Blinky is not running.")
        sys.exit(1)

    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        print("Blinky stopped.")
    except ProcessLookupError:
        os.remove(PID_FILE)
        print("Blinky stopped (process not found).")

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["start", "stop"]:
        print("Usage: blinky.py {start|stop}")
        sys.exit(1)

    if sys.argv[1] == "start":
        start_blinking()
    elif sys.argv[1] == "stop":
        stop_blinking()

if __name__ == "__main__":
    main()
