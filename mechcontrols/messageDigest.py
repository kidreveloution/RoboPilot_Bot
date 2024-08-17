import json

from gpiozero import OutputDevice, PWMOutputDevice

power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control
print (power_pin_forward,power_pin_reverse,pwm_power,pwm_steering)

def messageHandler(message):
    try:
        while True:
            if isinstance(message, list) and len(message) > 0 and isinstance(message[0], bytes):
                message = message[0].decode('utf-8')
            else:
                try:
                    message = message.decode('utf-8')
                except:
                    message = message
                    pass
        
            message = json.loads(message)
            command = message['msg_name']
            val = message['content']

            print(command,val)
            if command == "power":
                set_power(val)
            elif command == "steering":
                set_steering_pwm(val)

    except KeyboardInterrupt:
        print("Stopping motor and cleaning up GPIO")
        pwm_power.close()
        pwm_steering.close()
        power_pin_forward.close()
        power_pin_reverse.close()

    except Exception as e:
        print("An error occurred:", str(e))
        pwm_power.close()
        pwm_steering.close()
        power_pin_forward.close()
        power_pin_reverse.close()

def set_power(val):
    val = float(val)
    if val > 0:
        # Reverse
        power_pin_forward.off()
        power_pin_forward
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
            print("Steering value out of range. Please enter a number between 0>")
    except ValueError:
        print("Please enter a valid floating-point number for steering.")