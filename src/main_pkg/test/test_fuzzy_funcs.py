import pytest
import math
from fuzzy_pkg.fuzzy_funcs import MembershipFunction

t = MembershipFunction.trapezoidal
ARGS = (1.0, 2.0, 4.0, 5.0)

@pytest.mark.parametrize("x, expected", [
    (1.0, 0.0), (0.5, 0.0), (1.5, 0.5), (2.0, 1.0),
    (3.0, 1.0), (4.0, 1.0), (4.5, 0.5), (5.0, 0.0),
    (5.5, 0.0), (-100, 0.0), (1000, 0.0),
])
def test_trapezoidal_known_points(x, expected):
    assert math.isclose(t(x, *ARGS), expected)

@pytest.mark.parametrize("x", [i / 10 for i in range(-100, 101)])
def test_trapezoidal_always_in_unit_interval(x):
    assert 0.0 <= t(x, *ARGS) <= 1.0

def test_trapezoidal_shape_props():
    a, b, c, d = ARGS

    # Trapezoid: /---\
    # Left ramp from a to b ( / <- this one): membership must only ever increase.
    previous = t(a, a, b, c, d)
    for i in range(1, 51):
        x = a + (b - a) * i / 50
        current = t(x, a, b, c, d)
        assert current >= previous, f"left ramp decreased at x={x}"
        previous = current

    # Plateau ( --- <- this bit): membership must remain exactly 1.0.
    for i in range(0, 51):
        x = b + (c - b) * i / 50
        val = t(x, a, b, c, d)
        assert math.isclose(val, 1.0), f"plateau is not 1.0 at x={x}, got {val}"

    # Right ramp from c to d ( \ <- this one): membership must only ever decrease.
    previous = t(c, a, b, c, d)
    for i in range(0, 51):
        x = c + (d - c) * i / 50
        current = t(x, a, b, c, d)
        assert current <= previous, f"right ramp increased at X={x}"
        previous = current
