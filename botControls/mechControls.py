from gpiozero import OutputDevice, PWMOutputDevice
import json

# Motor Control Class
class MotorControl:
    def __init__(self):
        self.close_pwm_devices()
        self.initialized = False  # Initialization status
        self.current_power = 0  # Cached power value
        self.current_steering = 0.15  # Cached steering value
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
            if val == self.current_power:
                print(f"Power value unchanged: {val:.2f}")
                return  # Skip update if the value hasn't changed

            self.current_power = val
            if val > 0:  # Reverse
                self.power_pin_forward.off()
                self.power_pin_reverse.on()
            elif val < 0:  # Forward
                self.power_pin_forward.on()
                self.power_pin_reverse.off()
            else:  # Stop
                self.power_pin_forward.off()
                self.power_pin_reverse.off()
            self.pwm_power.value = abs(val) / 100
            print(f"Power PWM updated to: {val:.2f}")
        except ValueError:
            print("Invalid power value. Must be a number.")

    def set_steering_pwm(self, value):
        if not self.is_initialized():
            print("MotorControl is not initialized.")
            return

        try:
            value = float(value)
            if value == self.current_steering:
                print(f"Steering value unchanged: {value:.2f}")
                return  # Skip update if the value hasn't changed

            if 0.0 <= value <= 1.0:
                self.current_steering = value
                self.pwm_steering.value = value
                print(f"Steering PWM updated to: {value:.2f}")
            else:
                print("Steering value out of range (0.0 - 1.0).")
        except ValueError:
            print("Invalid steering value. Must be a floating-point number.")

    # Function to close all PWM output devices
    def close_pwm_devices(self):
        try:
            if motor_control.is_initialized():
                print("Closing PWM devices...")
                motor_control.pwm_power.close()
                motor_control.pwm_steering.close()
                motor_control.power_pin_forward.close()
                motor_control.power_pin_reverse.close()
                print("All GPIO devices closed successfully.")
            else:
                print("MotorControl is not initialized. No devices to close.")
        except Exception as e:
            print(f"Error while closing PWM devices: {e}")

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
