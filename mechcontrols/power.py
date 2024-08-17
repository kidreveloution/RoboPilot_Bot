import mechcontrols.pwmConfig
def set_power(val):
    val = float(val)
    if val > 0:
        # Reverse
        mechcontrols.pwmConfig.power_pin_forward.off()
        mechcontrols.pwmConfig.power_pin_forward
        mechcontrols.pwmConfig.power_pin_reverse.on()
        mechcontrols.pwmConfig.pwm_power.value = abs(val) / 100
    elif val < 0:
        # Forward
        mechcontrols.pwmConfig.power_pin_forward.on()
        mechcontrols.pwmConfig.power_pin_reverse.off()
        mechcontrols.pwmConfig.pwm_power.value = abs(val) / 100
    else:
        # Stop
        mechcontrols.pwmConfig.power_pin_forward.off()
        mechcontrols.pwmConfig.power_pin_reverse.off()
        mechcontrols.pwmConfig.pwm_power.value = 0