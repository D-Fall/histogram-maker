from numpy import mean, std, linspace
from scipy.stats import norm


def get_normal_pdf_axes(
    start: float,
    end: float,
    mean: float = 0,
    std: float = 1,
    graph_smoothness: int = 100,
) -> tuple[list[float], ...]:
    """
    Generate the x and y values, i.e. the axes, for the normal probability
    density function.
    """
    x = list(linspace(start, end, graph_smoothness))
    y = list(norm.pdf(x, mean, std))

    return x, y


def calculate_basic_stats(data: list[float]) -> tuple[float, float]:
    """
    Wrapper arround numpy's mean and std functions. Returns a tuple with the
    mean and standard deviation of a list of floats or similar.
    """
    mean_value = float(mean(data))
    std_value = float(std(data))
    return mean_value, std_value
