from numpy import array, linspace
from scipy.stats import norm


def norm_axes(
    start: int,
    end: int,
    mean: float = 0,
    std: float = 1,
    graph_smoothness: int = 100,
) -> tuple[array, array]:
    """
    Generate the x and y values, i.e. the axes, for the normal probability
    density function.
    """
    x = linspace(start, end, graph_smoothness)
    y = norm.pdf(x, mean, std)

    return x, y
