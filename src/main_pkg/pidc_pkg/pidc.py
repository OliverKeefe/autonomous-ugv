

class PIDController:
    """Class for Proportional-Integral-Derivative Controller."""
    def __init__(self):
        # Kp - proportional gain.
        self.kp = None
        # Ki - integral gain.
        self.ki= None
        # Kd - derivative gain
        self.kd = None
        # dt - loop interval time (assumes reasonable scale)
        self.dt = None
        # prev_err = previous error
        self.prev_err = 0
        # integral - integral, duh.
        self.integral = 0

    def control(
            self,
            setpoint,
            measured_val,
            kp,
            ki,
            kd,
            prev_err,
            integral,
            dt
    ):
        while True:
            err = (setpoint - measured_val)
            self.kp = err
            self.integral += err * self.dt
            derivative = (err - prev_err) / dt
            control = kp * err + ki * integral + kd * derivative
            return control, err, integral

    def get_setpoint(self):
        pass

    def update_kp(self, new_kp):
        self.kp = new_kp

    def curr_kp(self):
        return self.kp

    def update_ki(self, new_ki):
        self.ki = new_ki

    def curr_ki(self):
        return self.ki

    def update_kd(self, new_kd):
        self.kd = new_kd

    def curr_kd(self):
        return self.kd

    def update_dt(self, new_dt):
        self.dt = new_dt

    def curr_dt(self):
        return self.dt