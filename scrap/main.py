import mechcontrols.messageDigest
import modules.zmqHeader as zmqHeader
import modules.messageBuilder as messageBuilder
from mechcontrols.messageDigest import MotorControl

# Create the ZeroMQ connection object
zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="RoboCar_1",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=mechcontrols.messageDigest.messageHandler,
)

try:
    motor_control = MotorControl()  # Initialize the motor control

    # Connect to the ZeroMQ server
    print(zmqObj.connectZMQ())
    
    # Start the listening thread
    print(zmqObj.startListenThread())

    # Keep the main thread alive so that the listener can run
    while True:
        pass

except KeyboardInterrupt:
    print("KeyboardInterrupt received, closing ZeroMQ connection...")
    
    # Close the ZeroMQ socket and context gracefully
    zmqObj.close()  # You may need to implement this method in your ZMQ_CONNECTION class to handle graceful shutdown

    print("ZeroMQ connection closed.")

