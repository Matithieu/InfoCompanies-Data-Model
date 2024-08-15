#!/bin/bash

# Initialize iteration counter
iteration=0

# Trap Ctrl+C (SIGINT) and print the final iteration count
trap 'echo "Script interrupted after $iteration iterations, exiting..."; exit' SIGINT

while true; do
    # Increment iteration counter
    ((iteration++))

    # Start the Python script
    python3 Parsing/parsing.py &

    # Get the PID of the Python process
    PID=$!

    # Wait for 4 minutes
    sleep 240

    # Kill the Python process if CAPTCHA not encountered
    if kill -0 $PID 2>/dev/null; then
        kill $PID
    fi

    # Wait for the process to stop completely
    wait $PID 2>/dev/null

    # Wait 20 seconds before restarting
    sleep 20
done
