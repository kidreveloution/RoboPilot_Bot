import json
from gpiozero import OutputDevice, PWMOutputDevice
import RPi.GPIO as GPIO

GPIO.cleanup() 
# GPIO pin setup
power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control

def messageHandler(message):
    try:
        if isinstance(message, str):
            message = json.loads(message)

        print(message)

        command = str(message["msg_name"])
        val = str(message["content"])

        print(command, val)
        if command == "power":
            set_power(val)
        elif command == "steering":
            set_steering_pwm(val)

    except KeyboardInterrupt:
        print("Stopping motor and cleaning up GPIO")
        cleanup_gpio()

    except Exception as e:
        print("An error occurred:", str(e))
        cleanup_gpio()

def set_power(val):
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

def set_steering_pwm(value):
    try:
        value = float(value)
        if 0.0 <= value <= 1.0:            
            pwm_steering.value = value
            print(f"Steering PWM value set to: {value:.2f}")
        else:
            print("Steering value out of range. Please enter a number between 0.0 and 1.0.")
    except ValueError:
        print("Please enter a valid floating-point number for steering.")

def cleanup_gpio():
    pwm_power.close()
    pwm_steering.close()
    power_pin_forward.close()
    power_pin_reverse.close()

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
