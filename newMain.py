import json
import threading
import requests
import zmq
from gpiozero import OutputDevice, PWMOutputDevice
import modules.messageBuilder as messageBuilder


# Motor Control Class
class MotorControl:
    def __init__(self):
        self.initialized = False  # Initialization status
        try:
            print("Initializing GPIO devices...")
            self.power_pin_forward = OutputDevice(17, initial_value=False)
            self.power_pin_reverse = OutputDevice(27, initial_value=False)
            self.pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)
            self.pwm_steering = PWMOutputDevice(12)
            self.initialized = True  # Mark initialization as successful
            print("GPIO devices initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize GPIO devices: {e}")

    def is_initialized(self):
        return self.initialized

    def set_power(self, val):
        if not self.is_initialized():
            print("MotorControl is not initialized.")
            return
        try:
            val = float(val)
            if val > 0:  # Reverse
                self.power_pin_forward.off()
                self.power_pin_reverse.on()
            elif val < 0:  # Forward
                self.power_pin_forward.on()
                self.power_pin_reverse.off()
            else:  # Stop
                self.power_pin_forward.off()
                self.power_pin_reverse.off()
            print(f"Power PWM set to: {val:.2f}")
            self.pwm_power.value = abs(val) / 100
        except ValueError:
            print("Invalid power value. Must be a number.")

    def set_steering_pwm(self, value):
        if not self.is_initialized():
            print("MotorControl is not initialized.")
            return
        try:
            value = float(value)
            if 0.0 <= value <= 1.0:
                self.pwm_steering.value = value
                print(f"Steering PWM set to: {value:.2f}")
            else:
                print("Steering value out of range (0.0 - 1.0).")
        except ValueError:
            print("Invalid steering value. Must be a floating-point number.")


# Motor control instance
motor_control = MotorControl()


# Message Handler
def messageHandler(message):
    try:
        if not message:
            print("Received an empty message.")
            return  # Ignore empty messages

        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON received: {message}. Error: {e}")
                return  # Ignore invalid JSON messages

        command = message.get("msg_name")
        value = message.get("content")

        if not command or value is None:
            print(f"Message missing required fields: {message}")
            return

        if command == "power":
            motor_control.set_power(value)
        elif command == "steering":
            motor_control.set_steering_pwm(value)

    except Exception as e:
        print(f"Error in message handler: {e}")


# ZeroMQ Connection Class
class ZMQ_CONNECTION:
    def __init__(self, TX_ID, RX_ID, SERVER_IP, message_handler=None):
        if not TX_ID or not RX_ID or not SERVER_IP:
            raise ValueError("TX_ID, RX_ID, and SERVER_IP are required.")

        self.TX_ID = TX_ID
        self.RX_ID = RX_ID
        self.SERVER_IP = SERVER_IP
        self.context = zmq.Context()
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.setsockopt(zmq.IDENTITY, self.TX_ID.encode('utf-8'))
        self.message_handler = message_handler
        self.running = False

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch public IP: {e}")
            return "0.0.0.0"

    def registerAtRouter(self):
        try:
            return messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name="register",
                rx_id=self.RX_ID,
                content={"ip_address": self.get_public_ip()}
            ).buildMessage()
        except Exception as e:
            print(f"Error building registration message: {e}")
            return ""

    def connectZMQ(self):
        try:
            self.dealer.connect(self.SERVER_IP)
            registration_message = self.registerAtRouter()
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), registration_message.encode('utf-8')])
            print("Connected to ZeroMQ server.")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def listen(self):
        try:
            while self.running:
                message = self.dealer.recv_multipart()
                if message and self.message_handler:
                    self.message_handler(message[0].decode('utf-8'))
        except Exception as e:
            print(f"Error while listening: {e}")

    def sendMessage(self, RX_ID, msg_name, content):
        try:
            if isinstance(content, str):
                content = json.loads(content)
            msg = messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name=msg_name,
                rx_id=RX_ID,
                content=content
            ).buildMessage()
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), msg.encode('utf-8')])
        except Exception as e:
            print(f"Error sending message: {e}")

    def startListenThread(self):
        self.running = True
        threading.Thread(target=self.listen, daemon=True).start()

    def stopListenThread(self):
        self.running = False

    def close(self):
        self.stopListenThread()
        self.dealer.close()
        self.context.term()
        print("ZMQ connection closed.")


# Main Script
if __name__ == "__main__":
    zmqObj = ZMQ_CONNECTION(
        TX_ID="RoboCar_1",
        RX_ID="ROUTER",
        SERVER_IP="tcp://3.22.90.156:5555",
        message_handler=messageHandler,
    )

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
