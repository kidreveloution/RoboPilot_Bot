from gpiozero import OutputDevice, PWMOutputDevice

power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
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