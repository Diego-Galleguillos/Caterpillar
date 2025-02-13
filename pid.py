
class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0, sample_time=1.0, output_limits=(-1, 1)):
        """
        Initialize the PID controller with constants and other parameters.
        
        Parameters:
            kp (float): Proportional gain
            ki (float): Integral gain
            kd (float): Derivative gain
            setpoint (float): Desired target value
            sample_time (float): Time interval between control updates
            output_limits (tuple): The (min, max) limits for the control output
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.sample_time = sample_time
        self.output_limits = output_limits
        
        # State variables
        self.prev_error = 0
        self.integral = 0

    def compute(self, current_value):
        """
        Compute the control output based on the current value.

        Parameters:
            current_value (float): The current value from the system
        
        Returns:
            float: Control output (e.g., motor speed or adjustment)
        """
        # Calculate error
        error = self.setpoint - current_value
        
        # Proportional term
        proportional = self.kp * error
        
        # Integral term
        self.integral += error * self.sample_time
        integral = self.ki * self.integral
        
        # Derivative term
        derivative = self.kd * (error - self.prev_error) / self.sample_time
        
        # Compute total output
        output = proportional + integral + derivative
        
        # Apply output limits to ensure the output is within the desired range
        output = max(self.output_limits[0], min(output, self.output_limits[1]))
        
        # Save current error for next derivative calculation
        self.prev_error = error
        
        return output

    def set_setpoint(self, setpoint):
        """Set a new target setpoint for the controller."""
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0
