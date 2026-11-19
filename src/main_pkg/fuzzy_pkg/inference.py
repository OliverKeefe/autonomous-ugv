import math
from dataclasses import dataclass
from typing import List

from fuzzy_pkg.types import FuzzySet


class __Inference:
    def __init__(self):
        pass

    def fuzzify_all(self):
        pass

    def _build_sample_points(self):
        pass

class Sugeno(__Inference):
    def __init__(self):
        pass


class Mamdani(__Inference):
    def __init__(self):
        pass

    def _firing_strength(self):
        pass

    def _optimize(self):
        pass

    def _implicate(self):
        pass

    def _aggregate(self):
        pass

    def defuzzify(self):
        pass

class LinguisticVariable:
    def __init__(self, name: str, universe: tuple[float, float]):
        self.name = name
        self.universe = universe
        self.terms: dict[str, FuzzySet] = {}

    def add_term(self, term_name: str, fuzzy_set: FuzzySet) -> None:
        pass

    def fuzzify(self, x: float) -> dict[str, float]:
        pass

@dataclass
class Rule:
    antecedents: List[tuple[str, str]]
    consequent: str
    operator: str = "AND"
    weight: float = 1.0