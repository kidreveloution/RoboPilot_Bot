import json
from mechcontrols.steering import set_steering_pwm
from mechcontrols.power import set_power
from mechcontrols.PWM import MotorController

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
        MotorController.pwm_power.close()
        MotorController.pwm_steering.close()
        MotorController.power_pin_forward.close()
        MotorController.power_pin_reverse.close()

    except Exception as e:
        print("An error occurred:", str(e))
        MotorController.pwm_power.close()
        MotorController.pwm_steering.close()
        MotorController.power_pin_forward.close()
        MotorController.power_pin_reverse.close()