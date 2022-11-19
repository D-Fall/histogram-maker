from numpy import array, linspace
from scipy.stats import norm


def norm_axes(
    start: int,
    end: int,
    mean: float = 0,
    std: float = 1,
) -> tuple[array, array]:
    # TODO: maybe not hardcode 100
    # instead, make a graph_smoothness config
    x = linspace(start, end, 100)
    y = norm.pdf(x, mean, std)

    return x, y
