import pwmConfig
def set_power(val):
    val = float(val)
    if val > 0:
        # Reverse
        pwmConfig.power_pin_forward.off()
        pwmConfig.power_pin_forward
        pwmConfig.power_pin_reverse.on()
        pwmConfig.pwm_power.value = abs(val) / 100
    elif val < 0:
        # Forward
        pwmConfig.power_pin_forward.on()
        pwmConfig.power_pin_reverse.off()
        pwmConfig.pwm_power.value = abs(val) / 100
    else:
        # Stop
        pwmConfig.power_pin_forward.off()
        pwmConfig.power_pin_reverse.off()
        pwmConfig.pwm_power.value = 0