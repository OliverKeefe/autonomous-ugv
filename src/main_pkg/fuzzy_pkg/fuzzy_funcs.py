from dataclasses import dataclass
import math

@dataclass
class FuzzySet:
    elements: set

class MembershipFunction:
    @staticmethod
    def trapezoidal(x: float | int, a: float | int, b: float | int,
                    c: float | int, d: float | int) -> float:
        return max(0.0, min((x - a) / (b - a), 1.0, (d - x) / (d - c)))

    @staticmethod
    def triangular(x: float | int, a: float | int,
                   b: float | int, c: float | int) -> float:
        return max(0.0, min((x - a) / (b - a), 1.0, (c - x) / (c - b)))

    @staticmethod
    def gaussian(x: float | int, c: float | int, sigma: float | int) -> float:
        if sigma == 0:
            raise ValueError("sigma can't be 0.")

        # e - Euler's number.
        e = math.e
        dist_from_c = x - c
        scale_by_width = dist_from_c / sigma
        square_scale = scale_by_width ** 2

        negative_expo = -square_scale
        gauss = e ** negative_expo

        return gauss

    @staticmethod
    def singleton():
        pass

    @staticmethod
    def sigmoidal(x: float | int, a: float | int, c: float | int) -> float:
        e = math.e
        return 1 / (1 + e**-a * (x - c))
