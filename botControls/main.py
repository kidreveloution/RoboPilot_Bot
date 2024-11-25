import zmq
from zmqHeader import ZMQ_CONNECTION
from mechControls import messageHandler
# Main Script
if __name__ == "__main__":
    zmqObj = ZMQ_CONNECTION(
        TX_ID="RoboCar_1",
        RX_ID="ROUTER",
        SERVER_IP="tcp://3.22.90.156:5555",
        message_handler=messageHandler,
    )

    zmqObj.setsockopt(zmq.RCVHWM, 10)  # Limit the receive queue

    try:
        if zmqObj.connectZMQ():
            zmqObj.startListenThread()
            print("Listening for messages...")

            # Keep the main thread alive
            while True:
                pass
    except KeyboardInterrupt:
        print("Shutting down...")
        zmqObj.close()
