from gpiozero import OutputDevice, PWMOutputDevice

class MotorController:
    power_pin_forward = None
    power_pin_reverse = None
    pwm_power = None
    pwm_steering = None

    @classmethod
    def initialize(cls):
        cls.power_pin_forward = OutputDevice(17, initial_value=False)  # Direction pin 1 for forward
        cls.power_pin_reverse = OutputDevice(27, initial_value=False)  # Direction pin 2 for reverse
        cls.pwm_power = PWMOutputDevice(18, frequency=1000, initial_value=0)  # PWM pin for power control
        cls.pwm_steering = PWMOutputDevice(12)  # PWM pin for steering control

    @staticmethod
    def set_power_forward(value):
        if MotorController.power_pin_forward is not None:
            MotorController.power_pin_forward.value = value

    @staticmethod
    def set_power_reverse(value):
        if MotorController.power_pin_reverse is not None:
            MotorController.power_pin_reverse.value = value

    @staticmethod
    def set_pwm_power(value):
        if MotorController.pwm_power is not None:
            MotorController.pwm_power.value = value

    @staticmethod
    def set_pwm_steering(value):
        if MotorController.pwm_steering is not None:
            MotorController.pwm_steering.value = value


