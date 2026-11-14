from fuzzy_funcs import MembershipFunction as mf

class TrapezoidalFuzzySet:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def membership(self, input_val: float | int) -> float:
        return mf.trapezoidal(input_val, self.a, self.b, self.c, self.d)

class TriangularFuzzySet:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def membership(self, input_val: float | int) -> float:
        return mf.triangular(input_val, self.a, self.b, self.c)

class GaussianFuzzySet:
    def __init__(self, c, sigma):
        self.c = c
        self.sigma = sigma

    def membership(self, input_val: float | int) -> float:
        return mf.gaussian(input_val, self.c, self.sigma)

class SingletonFuzzySet:
    def __init__(self, c):
        self.c = c

    def membership(self, input_val: float | int):
        return mf.singleton(input_val, self.c)

class SigmoidalFuzzySet:
    def __init__(self, a, c):
        self.a = a
        self.c = c

    def membership(self, input_val: float | int):
        return mf.sigmoidal(input_val, self.a, self.c)