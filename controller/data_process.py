from numpy import mean, std


def get_stats(data: list[float]) -> tuple[float, float]:
    """
    Wrapper arround numpy's mean and std functions. Returns a tuple with this
    values provided a list of floats.
    """
    return mean(data), std(data)
