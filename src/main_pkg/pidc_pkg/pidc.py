import time
import pidc_pkg.types as t
import pidc_pkg.utils as utils


class PIDController:
    """Class for Proportional-Integral-Derivative Controller."""
    def __init__(self, kp=0.0, ki=0.0, kd=0.0,
                 out_limits=(-1e9, 1e9), integral_limits=(-1.0, 1.0), dt=0.0):
        # Kp - proportional gain.
        self.kp = kp
        # Ki - integral gain.
        self.ki= ki
        # Kd - derivative gain
        self.kd = kd
        # dt - loop interval time (assumes reasonable scale)
        self.dt: t.DeltaTime = dt
        # prev_err = previous error
        self.prev_err = 0
        # integral - integral, duh. Represents running sum of the past error.
        self.integral = 0
        self.out_limits = out_limits
        self.integral_limits = integral_limits #(-float('inf'), float('inf'))
        self._last_time = None
        self._prev_measured = None
        self.candidate = None

    def control(self, setpoint, measured_val):
        # now must be monotonic not time.Time as monotonic cant go backwards.
        now = time.monotonic()

        if self._last_time is not None:
            dt = now - self._last_time
        else:
            dt = self.dt
        dt = max(1e-3, min(dt, 0.5))
        self._last_time = now

        err = setpoint - measured_val
        #self.kp = err

        derivative = 0.0
        if self._prev_measured is not None:
            derivative = (err - self.prev_err) / dt
        self._prev_measured = measured_val
        self.prev_err = err

        _proportional = self.kp * err
        _integral = self.integral
        _derivative = self.kd * derivative

        out_lo, out_hi = self.out_limits
        integral_lo, integral_hi = self.integral_limits

        self.candidate = max(integral_lo, min(integral_hi, (self.integral + (err * dt))))
        self.integral_clamp(_proportional, out_hi, out_lo, _derivative, err)


        #self.integral += err * dt
        #low, high = self.integral_limits  # Prevents windup.
        #self.integral = max(low, min(high, self.integral))

        _integral = self.ki * self.integral
        control = max(out_lo, min(out_hi, _proportional + _integral + _derivative))

        return control

    def integral_clamp(self, p, ohi, olo, d, e):
        if (p + self.ki * self.candidate + d > ohi and e > 0) or \
                (p + self.ki * self.candidate + d < olo and e < 0):
            self.candidate = self.integral
        self.integral = self.candidate

    def reset(self):
        self.integral = 0.0
        self.prev_err = 0
        self._prev_measured = None
        self._last_time = None

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