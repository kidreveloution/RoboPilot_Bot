import json
from gpiozero import OutputDevice, PWMOutputDevice, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Reset GPIO state in case of prior unclean exits
Device.pin_factory.reset()

# Pin factory for improved PWM support
factory = PiGPIOFactory()

# GPIO pin setup
time.sleep(0.1)  # Delay for GPIO initialization
power_pin_forward = OutputDevice(17, initial_value=False)
power_pin_reverse = OutputDevice(27, initial_value=False)
pwm_power = PWMOutputDevice(18, frequency=500, initial_value=0, pin_factory=factory)  # Adjusted frequency
pwm_steering = PWMOutputDevice(12, pin_factory=factory)

def cleanup_gpio():
    """
    Clean up GPIO resources to ensure proper shutdown.
    """
    try:
        pwm_power.close()
        pwm_steering.close()
        power_pin_forward.close()
        power_pin_reverse.close()
        print("GPIO resources cleaned up successfully.")
    except Exception as e:
        print(f"Error during GPIO cleanup: {e}")


def messageHandler(message):
    """
    Handles incoming messages to control power and steering.

    :param message: JSON string or dictionary with 'msg_name' and 'content' keys
    """
    try:
        if isinstance(message, str):
            message = json.loads(message)

        print(f"Received message: {message}")

        command = str(message["msg_name"])
        val = str(message["content"])

        print(f"Command: {command}, Value: {val}")

        if command == "power":
            set_power(val)
        elif command == "steering":
            set_steering_pwm(val)

    except KeyboardInterrupt:
        print("Stopping motor and cleaning up GPIO.")
        cleanup_gpio()
        raise  # Re-raise to handle outside the function

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_gpio()


def set_power(val):
    """
    Set power level and direction.

    :param val: A float value where positive is forward, negative is reverse, and 0 is stop.
    """
    try:
        val = float(val)
        if val > 0:
            # Reverse
            power_pin_forward.off()
            power_pin_reverse.on()
            pwm_power.value = abs(val) / 100
        elif val < 0:
            # Forward
            power_pin_forward.on()
            power_pin_reverse.off()
            pwm_power.value = abs(val) / 100
        else:
            # Stop
            power_pin_forward.off()
            power_pin_reverse.off()
            pwm_power.value = 0
        print(f"Power set to: {val}")
    except ValueError:
        print("Invalid value for power. Please provide a float.")


def set_steering_pwm(value):
    """
    Set the steering PWM value.

    :param value: A float between 0.0 and 1.0.
    """
    try:
        value = float(value)
        if 0.0 <= value <= 1.0:
            pwm_steering.value = value
            print(f"Steering PWM value set to: {value:.2f}")
        else:
            print("Steering value out of range. Please enter a number between 0.0 and 1.0.")
    except ValueError:
        print("Please enter a valid floating-point number for steering.")


if __name__ == "__main__":
    try:
        print("Testing steering functionality.")
        while True:
            user_input = input("Enter a steering value between 0.0 and 1.0 (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting steering test.")
                break
            try:
                set_steering_pwm(user_input)
            except ValueError:
                print("Invalid input. Please enter a number between 0.0 and 1.0.")
    except KeyboardInterrupt:
        print("\nExiting test due to keyboard interrupt.")
    finally:
        print("Cleaning up GPIO resources.")
        cleanup_gpio()
