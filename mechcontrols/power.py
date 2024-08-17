from mechcontrols.PWM import power_pin_forward, power_pin_reverse, pwm_power, pwm_steering

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