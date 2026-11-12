import time
import pidc_pkg.types as t
import pidc_pkg.utils as utils


class PIDController:
    """Class for Proportional-Integral-Derivative Controller."""
    def __init__(self, kp=0.0, ki=0.0, kd=0.0, dt=0.0):
        # Kp - proportional gain.
        self.kp = kp
        # Ki - integral gain.
        self.ki= ki
        # Kd - derivative gain
        self.kd = kd
        # dt - loop interval time (assumes reasonable scale)
        self.dt: t.DeltaTime = 0.0
        # prev_err = previous error
        self.prev_err = 0
        # integral - integral, duh. Represents running sum of the past error.
        self.integral = 0

        self.integral_limits = (-float('inf'), float('inf'))

        self._last_time = None

    def control(self, setpoint, measured_val):

        # now must be monotonic not time.Time as monotonic cant go backwards.
        now = time.monotonic()

        if self._last_time is not None:
            dt = now - self._last_time
        else:
            dt = self.dt

        dt = utils.prevent_div_by_zero(dt)

        #while True:
        err = (setpoint - measured_val)
        #self.kp = err

        self.integral += err * dt
        low, high = self.integral_limits # Prevents windup.
        self.integral = max(low, min(high, self.integral))

        # TODO: 'derivative = -(measured - prev_measured) / dt' probably works better here, must test.
        derivative = (err - self.prev_err) / dt

        control = self.kp * err + self.ki * self.integral + self.kd * derivative
        self.prev_err = err
        self._last_time = now
        return control


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