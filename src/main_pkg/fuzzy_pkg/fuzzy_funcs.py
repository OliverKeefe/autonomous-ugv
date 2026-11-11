from dataclasses import dataclass

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
    def gaussian():
        pass

    @staticmethod
    def singleton():
        pass

    @staticmethod
    def sigmoidal():
        pass