import zmq
import requests
import json
import time
import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import common.messageBuilder as messageBuilder
import common.zmqHeader as zmqHeader

def printIncoming(msg):
    print(msg)

zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="fake_worker_1",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=printIncoming,
)

zmqObj.connectZMQ()
zmqObj.startListenThread()

# Generate fake GPS coordinates
def generate_fake_gps():
    # Randomly generate coordinates near a specific point
    base_lat = 42.2808  # Base latitude (e.g., near Ann Arbor, MI)
    base_lon = -83.7430  # Base longitude

    lat_variation = random.uniform(-0.01, 0.01)
    lon_variation = random.uniform(-0.01, 0.01)

    return {
        "latitude": base_lat + lat_variation,
        "longitude": base_lon + lon_variation
    }

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text


try:
    print("Trying")
    while True:
        fake_gps_data = generate_fake_gps()
        zmqObj.sendMessage(
            RX_ID="MOTHER",
            msg_name="gps_data",
            content=fake_gps_data
        )
        time.sleep(5)  # Adjust the sleep interval as needed
except KeyboardInterrupt:
    print("Stopping...")

except Exception as e:
    print("ERROR")

    print("An error occurred:", str(e))
