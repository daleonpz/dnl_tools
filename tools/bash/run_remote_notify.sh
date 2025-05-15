#!/bin/bash

# Configuration
REMOTE_USER="daniel"         # Remote server username
REMOTE_HOST="workstationmax"       # Remote server hostname or IP
REMOTE_SCRIPT="$1"                # Path to script/command on remote server

# Check if script/command is provided
if [ -z "$REMOTE_SCRIPT" ]; then
    echo "Usage: $0 /path/to/remote/script.sh"
    exit 1
fi

# Run the script on the remote server and capture exit status
ssh "$REMOTE_USER@$REMOTE_HOST" "$REMOTE_SCRIPT"
EXIT_STATUS=$?

# Display notification based on exit status
if [ $EXIT_STATUS -eq 0 ]; then
    notify-send "Script Finished" "The script $REMOTE_SCRIPT completed successfully on $REMOTE_HOST."
else
    notify-send "Script Failed" "The script $REMOTE_SCRIPT failed on $REMOTE_HOST with exit status $EXIT_STATUS."
fi

exit $EXIT_STATUS
