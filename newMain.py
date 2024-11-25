import json
from gpiozero import OutputDevice, PWMOutputDevice

class MotorControl:
    def __init__(self):
        # GPIO pin setup
        self.power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
        self.power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
        self.pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
        self.pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control

    def set_power(self, val):
        val = float(val)
        if val > 0:
            # Reverse
            self.power_pin_forward.off()
            self.power_pin_reverse.on()
            self.pwm_power.value = abs(val) / 100
        elif val < 0:
            # Forward
            self.power_pin_forward.on()
            self.power_pin_reverse.off()
            self.pwm_power.value = abs(val) / 100
        else:
            # Stop
            self.power_pin_forward.off()
            self.power_pin_reverse.off()
            self.pwm_power.value = 0

    def set_steering_pwm(self, value):
        try:
            value = float(value)
            if 0.0 <= value <= 1.0:
                self.pwm_steering.value = value
                print(f"Steering PWM value set to: {value:.2f}")
            else:
                print("Steering value out of range. Please enter a number between 0.0 and 1.0.")
        except ValueError:
            print("Please enter a valid floating-point number for steering.")

    def cleanup(self):
        self.pwm_power.close()
        self.pwm_steering.close()
        self.power_pin_forward.close()
        self.power_pin_reverse.close()

# Initialize the MotorControl instance on import
motor_control = MotorControl()

def messageHandler(message):
    print("RECEIVED INTO MECH CONTROLS")
    try:
        if isinstance(message, str):
            message = json.loads(message)

        print(message)

        command = str(message["msg_name"])
        val = str(message["content"])

        print(command, val)
        if command == "power":
            motor_control.set_power(val)
        elif command == "steering":
            motor_control.set_steering_pwm(val)

    except KeyboardInterrupt:
        print("Stopping motor and cleaning up GPIO")
        motor_control.cleanup()

    except Exception as e:
        print("An error occurred:", str(e))
        motor_control.cleanup()


import zmq
import sys
import os
import logging
import requests
import json
import threading
import modules.messageBuilder as messageBuilder

class ZMQ_CONNECTION:
    def __init__(self, TX_ID: str, RX_ID: str, SERVER_IP: str, message_handler=None) -> None:
        self.TX_ID = TX_ID
        self.RX_ID = RX_ID
        self.SERVER_IP = SERVER_IP
        self.context = zmq.Context()
        self.dealer = None
        self.message_handler = message_handler
        self.running = False  # Initialize the running flag
        
        if not TX_ID or not RX_ID or not SERVER_IP:
            raise ValueError("TX_ID, RX_ID, and SERVER_IP must be provided.")
    
    def get_public_ip(self) -> str:
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()  # Raises an error for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Failed to get public IP: {e}")
            return "0.0.0.0"  # Return a default IP if the request fails
    
    def connectZMQ(self) -> bool:
        try:
            self.dealer = self.context.socket(zmq.DEALER)
            self.dealer.setsockopt(zmq.IDENTITY, self.TX_ID.encode('utf-8'))
            self.dealer.connect(self.SERVER_IP)
            registration_message = self.registerAtRouter()
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), registration_message.encode('utf-8')])
            print("Connected and registration message sent.")
            return True
        except Exception as e:
            print(f"Failed to connect or send registration: {e}")
            return False
    
    def registerAtRouter(self) -> str:
        try:
            initial_message = messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name="register",
                rx_id=self.RX_ID,
                content={"ip_address": self.get_public_ip()}
            ).buildMessage()
            return initial_message
        except Exception as e:
            print(f"Failed to build registration message: {e}")
            return ""

    def listen(self):
        """Listens for incoming messages from the ROUTER socket."""
        try:
            while self.running:
                # Wait for incoming messages
                message = self.dealer.recv_multipart()
                if message:
                    print(f"Received message: {message}")
                    if self.message_handler:
                        self.message_handler(message[0].decode('utf-8'))  # Call the external handler
                        print(f"Sent to external Handler: {message[0].decode('utf-8')}")

        except Exception as e:
            print(f"Error while listening: {e}")
    
    def sendMessage(self, RX_ID, msg_name, content):
        if isinstance(content, str):
            content = json.loads(content)
        msg = messageBuilder.MESSAGE_CLASS(
            tx_id=self.TX_ID,
            msg_name=msg_name,
            rx_id=RX_ID,
            content=content
        ).buildMessage()
        self.dealer.send_multipart([self.TX_ID.encode('utf-8'), msg.encode('utf-8')])

    def startListenThread(self):
        self.running = True
        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.start()
    
    def stopListenThread(self):
        self.running = False
        if self.listenThread.is_alive():
            self.listenThread.join()
    
    def close(self):
        self.stopListenThread()
        if self.dealer:
            self.dealer.close()
        self.context.term()
        print("ZMQ connection closed.")
import modules.zmqHeader as zmqHeader

# Create the ZeroMQ connection object
zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="RoboCar_1",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=messageHandler,
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