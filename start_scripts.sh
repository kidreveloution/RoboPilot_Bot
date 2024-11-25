#!/bin/bash

# Function to check internet connectivity
check_internet() {
    # Ping Google's public DNS server with a timeout
    ping -c 1 -W 3 8.8.8.8 &> /dev/null
    return $?
}

# Function to start the Python scripts in screen sessions
start_scripts() {
    # Kill existing screen sessions with the same name if they exist
    screen -S script1_session -X quit &> /dev/null
    screen -S script2_session -X quit &> /dev/null

    # Start the first script in a new screen session
    screen -dmS script1_session bash -c "python3 /home/shahin/RoboPilot_Bot/botControls/cameraStart.py; exec bash"
    echo "Started script1.py in a new screen session."

    # Start the second script in a new screen session
    screen -dmS script2_session bash -c "python3 /home/shahin/RoboPilot_Bot/botControls/main.py; exec bash"
    echo "Started script2.py in a new screen session."

    # List all active screens
    screen -ls
}

# Main loop
while true; do
    if check_internet; then
        echo "Internet is available. Starting scripts..."
        start_scripts
        break
    else
        echo "No internet connection. Retrying in 10 seconds..."
        sleep 10
    fi
done

# Monitor internet connectivity and restart scripts if it goes down and comes back
while true; do
    if ! check_internet; then
        echo "Internet connection lost. Waiting to reconnect..."
        while ! check_internet; do
            sleep 10
        done
        echo "Internet reconnected. Restarting scripts..."
        start_scripts
    fi
    sleep 10
done
