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

if __name__ == "__main__":
    try:
        print("Testing steering functionality.")
        while True:
            user_input = input("Enter a steering value between 0.0 and 1.0 (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting steering test.")
                break
            try:
                motor_control.set_steering_pwm(user_input)
            except ValueError:
                print("Invalid input. Please enter a number between 0.0 and 1.0.")
    except KeyboardInterrupt:
        print("\nExiting test due to keyboard interrupt.")
    finally:
        print("Cleaning up GPIO resources.")
        motor_control.cleanup()
