
def prevent_div_by_zero(v: float | int):
    return max(v, 1e-6)
