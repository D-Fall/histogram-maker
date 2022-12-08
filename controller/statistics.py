from numpy import array, mean, std, linspace
from scipy.stats import norm


def get_normal_pdf_axes(
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


def calculate_basic_stats(data: list[float]) -> tuple[float, float]:
    """
    Wrapper arround numpy's mean and std functions. Returns a tuple with the
    mean and standard deviation of a list of floats or similar.
    """
    return mean(data), std(data)
