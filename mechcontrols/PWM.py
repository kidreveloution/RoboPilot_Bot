from gpiozero import OutputDevice, PWMOutputDevice
power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 fo>
power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 fo>
pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for>
pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control
