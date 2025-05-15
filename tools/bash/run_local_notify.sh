#!/bin/bash

# Configuration
SCRIPT_PATH="$1"          # Path to the local script/command
USE_SUDO="$2"             # Optional: Pass "sudo" to run with sudo

# Check if script/command is provided
if [ -z "$SCRIPT_PATH" ]; then
    echo "Usage: $0 /path/to/script.sh [sudo]"
    exit 1
fi

# Run the script and capture exit status
if [ "$USE_SUDO" = "sudo" ]; then
    sudo bash -c "$SCRIPT_PATH"
    EXIT_STATUS=$?
else
    bash -c "$SCRIPT_PATH"
    EXIT_STATUS=$?
fi

# Display notification based on exit status
if [ $EXIT_STATUS -eq 0 ]; then
    notify-send "Script Finished" "The script $SCRIPT_PATH completed successfully."
else
    notify-send "Script Failed" "The script $SCRIPT_PATH failed with exit status $EXIT_STATUS."
fi

exit $EXIT_STATUS
