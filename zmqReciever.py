from gpiozero import OutputDevice, PWMOutputDevice
import zmq
import requests
import json
# Setup GPIO
power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 fo>
power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 fo>
pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for>
pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control

# Define function to set steering PWM correctly
def set_steering_pwm(value):
    """Set steering PWM value within the range of 0.0 to 1.0."""
    try:
        value = float(value)
        if 0.0 <= value <= 1.0:            
            pwm_steering.value = value
            print(f"Steering PWM value set to: {value:.2f}")
        else:
            print("Steering value out of range. Please enter a number between 0>")
    except ValueError:
        print("Please enter a valid floating-point number for steering.")


def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

# Setup ZeroMQ
SERVER_IP = '3.22.90.156'
WORKER_ID = "car_1"
PUBLIC_IP = get_public_ip()

context = zmq.Context()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://"+SERVER_IP+":5555")  # Use the server's IP address

dealer.send_multipart([PUBLIC_IP.encode('utf-8'),b''])

try:
    while True:
        message = dealer.recv_multipart()
        if isinstance(message, list) and len(message) > 0 and isinstance(message[0], bytes):
            message = message[0].decode('utf-8')
        else:
            message = message.decode('utf-8')
    
        message = json.loads(message)
        command = message['msg_name']
        val = message['content']

        print(command,val)
        if command == "power":
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
