from mechcontrols.PWM import MotorController

def set_power(val):
    val = float(val)
    if val > 0:
        # Reverse
        MotorController.power_pin_forward.off()
        MotorController.power_pin_forward
        MotorController.power_pin_reverse.on()
        MotorController.pwm_power.value = abs(val) / 100
    elif val < 0:
        # Forward
        MotorController.power_pin_forward.on()
        MotorController.power_pin_reverse.off()
        MotorController.pwm_power.value = abs(val) / 100
    else:
        # Stop
        MotorController.power_pin_forward.off()
        MotorController.power_pin_reverse.off()
        MotorController.pwm_power.value = 0