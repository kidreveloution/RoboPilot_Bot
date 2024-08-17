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