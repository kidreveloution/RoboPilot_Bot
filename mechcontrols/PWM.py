from gpiozero import OutputDevice, PWMOutputDevice

class MotorController:
    def __init__(self):
        self.power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
        self.power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
        self.pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
        self.pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control